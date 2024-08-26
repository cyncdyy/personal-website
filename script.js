/*loader*/
window.addEventListener("load", function() {
  document.querySelector(".loader").classList.add("loader--hidden");
});

// /* scroll snap */
// // Add smooth scrolling behavior
// document.querySelectorAll('a[href^="#"]').forEach(anchor => {
//   anchor.addEventListener('click', function (e) {
//     e.preventDefault();
//     document.querySelector(this.getAttribute('href')).scrollIntoView({
//       behavior: 'smooth'
//     });
//   });
// });

/* cursor */
document.getElementsByTagName("body")[0].addEventListener("mousemove", function(n) {
  t.style.left = n.clientX + "px", 
t.style.top = n.clientY + "px", 
e.style.left = n.clientX + "px", 
e.style.top = n.clientY + "px", 
i.style.left = n.clientX + "px", 
i.style.top = n.clientY + "px"
});
var t = document.getElementById("cursor"),
  e = document.getElementById("cursor2"),
  i = document.getElementById("cursor3");
function n(t) {
  e.classList.add("hover"), i.classList.add("hover")
}
function s(t) {
  e.classList.remove("hover"), i.classList.remove("hover")
}
s();
for (var r = document.querySelectorAll(".hover-target"), a = r.length - 1; a >= 0; a--) {
  o(r[a])
}
function o(t) {
  t.addEventListener("mouseover", n), t.addEventListener("mouseout", s)
}

/* fade in */
const fadeInElements = document.querySelectorAll('.fade-in');

function handleFadeInOnScroll() {
  fadeInElements.forEach(element => {
    const elementTop = element.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;

    if (elementTop < windowHeight * 0.8) {
      element.classList.add('visible');
    } else {
      element.classList.remove('visible');
    }
  });
}

window.addEventListener('scroll', handleFadeInOnScroll);


/* project image carousel */
const slider = document.querySelector('.slider');

function activate(e) {
  const items = document.querySelectorAll('.item');
  e.target.matches('.next') && slider.append(items[0])
  e.target.matches('.prev') && slider.prepend(items[items.length-1]);
}

document.addEventListener('click',activate,false);


/* typewrite */
var TxtType = function(el, toRotate, period) {
  this.toRotate = toRotate;
  this.el = el;
  this.loopNum = 0;
  this.period = parseInt(period, 10) || 2000;
  this.txt = '';
  this.isDeleting = false;
  this.isObserved = false;
};

TxtType.prototype.tick = function() {
  var i = this.loopNum % this.toRotate.length;
  var fullTxt = this.toRotate[i];

  if (this.isDeleting) {
      this.txt = fullTxt.substring(0, this.txt.length - 1);
  } else {
      this.txt = fullTxt.substring(0, this.txt.length + 1);
  }

  this.el.innerHTML = '<span class="wrap">' + this.txt + '</span>';

  var that = this;
  var delta = 200 - Math.random() * 100;

  if (this.isDeleting) { delta /= 2; }

  if (!this.isDeleting && this.txt === fullTxt) {
      delta = this.period;
      this.isDeleting = true;
  } else if (this.isDeleting && this.txt === '') {
      this.isDeleting = false;
      this.loopNum++;
      delta = 500;
  }

  setTimeout(function() {
      that.tick();
  }, delta);
};

TxtType.prototype.start = function() {
  this.tick();
};

window.onload = function() {
  var elements = document.getElementsByClassName('typewrite');
  for (var i = 0; i < elements.length; i++) {
      var toRotate = elements[i].getAttribute('data-type');
      var period = elements[i].getAttribute('data-period');
      if (toRotate) {
          var txtType = new TxtType(elements[i], JSON.parse(toRotate), period);

          var observer = new IntersectionObserver(function(entries) {
              entries.forEach(function(entry) {
                  if (entry.isIntersecting) {
                      txtType.isObserved = true;
                      txtType.start();
                  }
              });
          }, { rootMargin: '0px', threshold: 0.5 });

          observer.observe(elements[i]);
      }
  }

  // INJECT CSS
  var css = document.createElement("style");
  css.type = "text/css";
  css.innerHTML = ".typewrite > .wrap { border-right: 0.08em solid black; animation: typewriter 4s steps(40) infinite, blink 0.75s infinite; }";
  document.body.appendChild(css);
};


/* travel */
const state = {};
    const carouselList = document.querySelector('.carousel__list');
    const carouselItems = document.querySelectorAll('.carousel__item');
    const elems = Array.from(carouselItems);

    carouselList.addEventListener('click', function (event) {
      var newActive = event.target;
      var isItem = newActive.closest('.carousel__item');

      if (!isItem || newActive.classList.contains('carousel__item_active')) {
        return;
      }

      update(newActive);
    });

    const update = function(newActive) {
      const newActivePos = newActive.dataset.pos;

      const current = elems.find((elem) => elem.dataset.pos == 0);
      const prev1 = elems.find((elem) => elem.dataset.pos == -1);
      const prev2 = elems.find((elem) => elem.dataset.pos == -2);
      const prev3 = elems.find((elem) => elem.dataset.pos == -3);
      const next1 = elems.find((elem) => elem.dataset.pos == 1);
      const next2 = elems.find((elem) => elem.dataset.pos == 2);
      const next3 = elems.find((elem) => elem.dataset.pos == 3);

      current.classList.remove('carousel__item_active');

      [current, prev1, prev2, prev3, next1, next2, next3].forEach(item => {
        var itemPos = item.dataset.pos;

        item.dataset.pos = getPos(itemPos, newActivePos);
      });
    };

    const getPos = function (current, active) {
      const diff = current - active;

      if (Math.abs(current - active) > 3) {
        return -current;
      }

      return diff;
    };

// download button
window.onload = function() {
  setTimeout(function() {
    document.querySelectorAll('.fade-in').forEach(element => {
      element.classList.add('show');
    });
  }, 500); // Adjust the delay as needed
};

