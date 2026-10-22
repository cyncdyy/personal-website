# Destination Lab — three interactive prototypes

A portable, buildless HTML/CSS/JavaScript study website based on the three Skyscanner redesign concepts. No installation, API keys, frameworks, external assets, analytics, or paid services are required.

## Open locally

Open `index.html` in a modern browser. Keep the `assets` folder beside the HTML files. If your browser restricts local files, serve this folder using `python3 -m http.server 8000` and open `http://localhost:8000`.

## Put it on your existing personal website

1. Copy this entire folder into the directory your GitHub website publishes. You can rename it to `flight-study`.
2. Commit and push those files using your normal GitHub website workflow. If your site uses a framework, place the folder in its static/public directory so the files are copied without processing.
3. After your normal deployment completes, open the folder's `index.html` URL. For example, if your website is `https://YOUR-NAME.github.io/`, the URL would be `https://YOUR-NAME.github.io/flight-study/`. A project website may also have a repository-name segment before `flight-study/`.
4. Add a link from your personal website to that URL and share it with participants.

All internal links are relative, so the site works under a subfolder. The package does not replace your personal site's existing homepage. For a separate static repository, publish this package's contents as the site's root using your chosen GitHub Pages deployment configuration.

## Files

- `index.html`: landing page with three prototype buttons and the shared task.
- `prototype-a.html`: destination selection beside a live comparison table, two-item shortlist.
- `prototype-b.html`: airfare slider, direct/connecting preferences, interest filtering, no-results state, editable preferences, details and shortlist.
- `prototype-c.html`: interest categories, destination details, illustrative experiences, sample flight information and shortlist.
- `feedback.html`: brief feedback questionnaire with downloadable text responses.
- `assets/styles.css`: dark/mint portfolio landing theme and blue/white prototype layouts.
- `assets/app.js`: destination data, interface rendering and feedback export.
- `assets/interactions.js`: trip editing, shortlist dialogs and simulated flight selection.
- `assets/photo-match.css`: visual refinements matching the three supplied images.

## Feedback collection

This is a static website. **Nothing is submitted to you automatically.** Participants download a text file and send it to you using your existing contact method. Explain where they should send it when you invite them. The form says this explicitly; it is not a simulated online submission.

If you already have a Google Form or other collection form, replace links to `feedback.html` in the HTML and JavaScript with that form's URL. Avoid putting any private API keys into client-side code.

Shortlists are stored separately per prototype in the browser's session storage when available. There is no cross-device storage, participant tracking, or backend. Feedback text is not saved automatically and disappears when the page is refreshed or left.

## Study setup

Suggested invitation: “Please open the link, try prototypes A, B and C, and save two destinations you would consider in each. Imagine traveling from Hong Kong on 5–11 November 2026 with a HK$2,500 return-flight budget. After each prototype, use Give feedback, download your answers, and send me the file. The fares and flight details are fictional.”

Rotate the order between participants (ABC, BCA, CAB) to reduce order effects. The pages now match the supplied reference images: A has Taipei, Seoul and Tokyo; B has Seoul and Tokyo; C has Hanoi, Shanghai, Bali and Hokkaido. B groups destinations within and outside the selected budget. Fares in A and B intentionally differ to match the images. Standardize data before a controlled comparative study if content should not influence preferences.

The origin, dates and traveler count start with the study scenario and can be edited using the footer controls; fares remain fixed sample data. The interface does not perform live searches or bookings. Seasonal descriptions, flight times, baggage allowances, activities and fares are illustrative. Destination imagery is displayed from the supplied image mockups using CSS image windows. All image files are local to the package.

## Customize

Edit the `destinations` array at the top of `assets/app.js` to change data for all prototypes. Update the task text in `index.html` and the shared `top()` function in `app.js` if you change the study scenario. Change colors in the `:root` variables in `styles.css`.

## Verification

Passed JavaScript syntax checks, static asset/link checks, and isolated interaction-logic checks for comparison, shortlist limits, budget/interest filtering, empty results, skipping preferences, destination details and back navigation. Those checks used a minimal DOM harness, not a full browser.

Full browser rendering, responsive layout and the actual feedback download still require a manual check. The preview browser denied access to the local-file URL; no browser visual verification is claimed. Before sending invitations, open the uploaded site on desktop and phone, complete one flow in each prototype, then download and read a feedback file.

## Latest reference alignment

A = comparison, B = guided preferences, C = activity exploration. Landing-page links and feedback labels use this mapping. This supersedes the reversed A/B labels in the previous revision.

The layouts, visible destination sets, sample prices, headers and photo windows follow the latest supplied mockups. They remain HTML controls, not screenshot overlays. Origin and dates can be edited through the trip dialog. Header Hotels/Car hire labels provide visual context, not functional modules; the study is limited to destination selection. Use the footer links for the landing page and feedback.

Syntax, asset paths and isolated interaction checks passed after these changes. Browser visual matching has not been verified in this environment.
