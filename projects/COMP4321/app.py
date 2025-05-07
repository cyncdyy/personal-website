from flask import Flask, request, render_template, make_response, redirect, url_for
from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import math
import datetime
import json

nltk.download(['punkt', 'stopwords'])
nltk.download(['punkt', 'punkt_tab'])  # Add punkt_tab

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for sessions

    
# ----------------------
# Data Structures
# ----------------------
class Crawler:
    def __init__(self):
        self.visited = set()
        self.queue = []
        self.page_data = {}  # {url: {content, last_modified, size, links}}
        self.parent_child = defaultdict(list)

    def crawl(self, start_url, max_pages=300):
        self.queue = [start_url]
        while self.queue and len(self.visited) < max_pages:
            url = self.queue.pop(0)
            if url not in self.visited:
                try:
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Store page data
                    self.page_data[url] = {
                        'content': response.text,
                        'last_modified': response.headers.get('Last-Modified', datetime.datetime.now().isoformat()),
                        'size': len(response.text),
                        'title': soup.title.string if soup.title else url
                    }
                    
                    # Extract links
                    links = [a.get('href') for a in soup.find_all('a', href=True)]
                    absolute_links = [requests.compat.urljoin(url, link) for link in links]
                    self.parent_child[url] = absolute_links
                    self.queue.extend(absolute_links)
                    
                    self.visited.add(url)
                except:
                    continue

class Indexer:
    def __init__(self):
        self.stopwords = set(open('stopwords.txt').read().splitlines())
        self.stemmer = PorterStemmer()
        self.body_index = defaultdict(list)  # {term: [(doc_id, tf, positions)]}
        self.title_index = defaultdict(list)
        self.documents = {}  # {url: doc_id}
        self.doc_count = 0

    def process_page(self, url, content, title):
        doc_id = self.doc_count
        self.documents[url] = doc_id
        self.doc_count += 1
        
        # Process body
        body_terms = self._process_text(content)
        self._update_index(self.body_index, doc_id, body_terms)
        
        # Process title
        title_terms = self._process_text(title)
        self._update_index(self.title_index, doc_id, title_terms, is_title=True)

    def _process_text(self, text):
        tokens = word_tokenize(text.lower())
        filtered = [self.stemmer.stem(t) for t in tokens if t not in self.stopwords and t.isalnum()]
        return filtered

    def _update_index(self, index, doc_id, terms, is_title=False):
        tf = defaultdict(int)
        positions = defaultdict(list)
        for pos, term in enumerate(terms):
            tf[term] += 1
            positions[term].append(pos)
        
        max_tf = max(tf.values(), default=1)
        for term in tf:
            index[term].append((
                doc_id,
                tf[term]/max_tf,  # Normalized TF
                positions[term]
            ))

# ----------------------
# Query History Feature
# ----------------------
def get_query_history():
    return json.loads(request.cookies.get('query_history', '[]'))

def update_query_history(response, new_query):
    history = get_query_history()
    history = [q for q in history if q['query'] != new_query]
    history.insert(0, {
        'query': new_query,
        'time': datetime.datetime.now().isoformat()
    })
    history = history[:10]
    response.set_cookie('query_history', json.dumps(history), max_age=604800)


# ----------------------
# Initialize Components
# ----------------------
crawler = Crawler()
indexer = Indexer()

# Crawl and index test URL
crawler.crawl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm", max_pages=300)
for url in crawler.visited:
    content = crawler.page_data[url]['content']
    title = crawler.page_data[url]['title']
    indexer.process_page(url, content, title)

# ----------------------
# Search Engine
# ----------------------
class SearchEngine:
    def search(self, query, boost_terms=None, filter_docs=None):
        # Parse query
        terms = []
        in_phrase = False
        current_phrase = []
        
        for token in word_tokenize(query.lower()):
            if token == '"':
                in_phrase = not in_phrase
                if not in_phrase and current_phrase:
                    terms.append(('phrase', current_phrase))
                    current_phrase = []
            elif in_phrase:
                current_phrase.append(indexer.stemmer.stem(token))
            else:
                terms.append(('term', indexer.stemmer.stem(token)))
        
        # Calculate scores
        scores = defaultdict(float)
        for term_type, value in terms:
            if term_type == 'term':
                docs = indexer.body_index.get(value, []) + indexer.title_index.get(value, [])
                df = len(docs)
                for doc_id, tf, _ in docs:
                    idf = math.log(indexer.doc_count / (df + 1))
                    scores[doc_id] += tf * idf * (2 if 'title' in docs else 1)
            # Phrase handling would go here
        
        # Sort results
        if filter_docs:
            scores = {doc_id: score for doc_id, score in scores.items() 
                     if doc_id in filter_docs}
        
        if boost_terms:
            for doc_id in scores:
                url = next(url for url, id in indexer.documents.items() if id == doc_id)
                page_terms = self._get_page_terms(url)
                boost = sum(1 for term in boost_terms if term in page_terms)
                scores[doc_id] *= (1 + boost * 0.2)

        # Apply filtering for search within results
        if filter_docs:
            scores = {doc_id: score for doc_id, score in scores.items() 
                     if doc_id in filter_docs}

        return sorted(scores.items(), key=lambda x: -x[1])[:50]

    def _get_page_terms(self, url):
        content = crawler.page_data[url]['content']
        return indexer._process_text(content)
        

# ----------------------
# Helper Functions
# ----------------------
def process_results(doc_scores):
    results = []
    for doc_id, score in doc_scores:
        url = next(url for url, id in indexer.documents.items() if id == doc_id)
        page_data = crawler.page_data[url]
        keywords = sorted(indexer.body_index.items(),
                        key=lambda x: sum(tf for _, tf, _ in x[1] if x[1][0][0] == doc_id),
                        reverse=True)[:5]
        results.append({
            'score': round(score, 2),
            'title': page_data['title'],
            'url': url,
            'date': page_data['last_modified'],
            'size': f"{len(page_data['content']) // 1024}KB",
            'keywords': [f"{term} ({sum(tf for _, tf, _ in entries):.3f})"
             for term, entries in keywords]
        })
    return results

# ----------------------
# Web Interface
# ----------------------

@app.route('/clear-history', methods=['POST'])
def clear_history():
    resp = make_response(redirect(url_for('home')))
    resp.delete_cookie('query_history')
    return resp

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    if isinstance(value, str):
        try: value = datetime.datetime.fromisoformat(value)
        except: return value
    return value.strftime(format)


@app.route('/', methods=['GET'])
def home():
    query = request.args.get('query')
    similar_to = request.args.get('similar_to')
    merge_queries = request.args.getlist('merge_queries')
    search_within = request.args.get('search_within')
    
    engine = SearchEngine()
    results = []
    query_history = get_query_history()

    # Handle similar pages request
    if similar_to:
        try:
            content = crawler.page_data[similar_to]['content']
            terms = indexer._process_text(content)
            term_counts = defaultdict(int)
            for term in terms:
                term_counts[term] += 1
            top_terms = sorted(term_counts.items(), key=lambda x: (-x[1], x[0]))[:5]
            new_query = ' '.join([f'"{term}"' for term, _ in top_terms])
            doc_scores = engine.search(new_query, boost_terms=[term for term, _ in top_terms])
            
            # Get popular keywords
            keyword_freq = defaultdict(float)
            for term, postings in indexer.body_index.items():
                total_tf = sum(tf for _, tf, _ in postings)
                keyword_freq[term] = total_tf
            popular_keywords = sorted(keyword_freq.items(), key=lambda x: -x[1])

            results = process_results(doc_scores)
            return render_template('results.html', 
                                results=results,
                                query=new_query,
                                query_history=query_history,
                                popular_keywords=popular_keywords)  # Add this line
            
        except KeyError:
            return "Invalid page for similar search", 400


    # Handle merged queries
    if merge_queries:
        merged_scores = defaultdict(float)
        selected_queries = [query_history[int(i)]['query'] for i in merge_queries]
        for q in selected_queries:
            for doc_id, score in engine.search(q):
                merged_scores[doc_id] += score
        doc_scores = sorted(merged_scores.items(), key=lambda x: -x[1])[:50]
        results = process_results(doc_scores)

    # Handle search within results
    elif search_within:
        base_query = query_history[int(search_within)]['query']
        base_results = {doc_id for doc_id, _ in engine.search(base_query)}
        doc_scores = engine.search(query, filter_docs=base_results)
        results = process_results(doc_scores)

    # Normal search
    elif query:
        engine = SearchEngine()
        doc_scores = engine.search(query)
        for doc_id, score in doc_scores:
            url = next(url for url, id in indexer.documents.items() if id == doc_id)
            page_data = crawler.page_data[url]
            # Get top 5 keywords (stemmed)
            keyword_scores = []
            for term, postings in indexer.body_index.items():
                for posting in postings:
                    if posting[0] == doc_id:
                        tf = posting[1]
                        keyword_scores.append((term, tf))
                        break
            keywords = sorted(keyword_scores, key=lambda x: -x[1])[:5]
            results.append({
                'score': round(score, 2),
                'title': page_data['title'],
                'url': url,
                'date': page_data['last_modified'],
                'size': f"{len(page_data['content']) // 1024}KB",
                'keywords': [f"{term} ({round(tf,2)})" for term, tf in keywords]
            })

    # Popular stemmed keywords across all docs
    keyword_freq = defaultdict(float)
    for term, postings in indexer.body_index.items():
        total_tf = sum(tf for _, tf, _ in postings)
        keyword_freq[term] = total_tf
    popular_keywords = sorted(keyword_freq.items(), key=lambda x: -x[1])

    # Build response
    resp = make_response(render_template('results.html', 
                                       results=results,
                                       query=query,
                                       query_history=query_history, 
                                       popular_keywords=popular_keywords))
    
    # Update history for new queries
    if query and not merge_queries and not search_within:
        update_query_history(resp, query)
    
    return resp


if __name__ == '__main__':
    app.run()