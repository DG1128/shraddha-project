/* ============================================================
   SHRADDHA PRODUCTS - main.js
   Features: Slider, Mobile Nav, Dropdown Toggle, AJAX Forms
   ============================================================ */

(function () {
  'use strict';

  /* ── Navbar scroll shadow ─────────────────────────────────── */
  const header = document.getElementById('siteHeader');
  window.addEventListener('scroll', function () {
    if (header) header.classList.toggle('scrolled', window.scrollY > 30);
  }, { passive: true });

  /* ── Hamburger / Mobile Menu ──────────────────────────────── */
  const hamburger = document.getElementById('hamburger');
  const mainNav   = document.getElementById('mainNav');

  if (hamburger && mainNav) {
    hamburger.addEventListener('click', function () {
      const open = mainNav.classList.toggle('open');
      const spans = hamburger.querySelectorAll('span');
      if (open) {
        spans[0].style.transform = 'rotate(45deg) translate(5px,5px)';
        spans[1].style.opacity   = '0';
        spans[2].style.transform = 'rotate(-45deg) translate(5px,-5px)';
      } else {
        spans.forEach(function (s) { s.style.transform = ''; s.style.opacity = ''; });
      }
    });

    /* Mobile dropdown toggle */
    const dropItem = mainNav.querySelector('.has-dropdown');
    if (dropItem) {
      dropItem.querySelector('a').addEventListener('click', function (e) {
        if (window.innerWidth <= 768) {
          e.preventDefault();
          dropItem.classList.toggle('open');
        }
      });
    }

    /* Close nav on outside click */
    document.addEventListener('click', function (e) {
      if (!header.contains(e.target)) {
        mainNav.classList.remove('open');
        hamburger.querySelectorAll('span').forEach(function (s) { s.style.transform = ''; s.style.opacity = ''; });
      }
    });
  }

  /* ── Hero Slider ──────────────────────────────────────────── */
  const slides  = document.querySelectorAll('.slide');
  const dots    = document.querySelectorAll('.dot');
  const prevBtn = document.getElementById('slidePrev');
  const nextBtn = document.getElementById('slideNext');

  if (slides.length > 1) {
    let current = 0;
    let timer;

    function goTo(idx) {
      slides[current].classList.remove('active');
      dots[current] && dots[current].classList.remove('active');
      current = (idx + slides.length) % slides.length;
      slides[current].classList.add('active');
      dots[current] && dots[current].classList.add('active');
    }

    function startAuto() {
      timer = setInterval(function () { goTo(current + 1); }, 4500);
    }

    function resetAuto() {
      clearInterval(timer);
      startAuto();
    }

    if (prevBtn) prevBtn.addEventListener('click', function () { goTo(current - 1); resetAuto(); });
    if (nextBtn) nextBtn.addEventListener('click', function () { goTo(current + 1); resetAuto(); });

    dots.forEach(function (dot) {
      dot.addEventListener('click', function () {
        goTo(parseInt(dot.dataset.idx));
        resetAuto();
      });
    });

    startAuto();
  }

  /* ── AJAX Form Handler ────────────────────────────────────── */
  function handleForm(formId, successId) {
    var form = document.getElementById(formId);
    var success = document.getElementById(successId);
    if (!form) return;

    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      var origText = btn.textContent;
      btn.textContent = 'Sending...';

      try {
        var payload = Object.fromEntries(new FormData(form));
        var resp = await fetch('/api/enquiry', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        var data = await resp.json();
        if (data.status === 'success') {
          form.reset();
          if (success) { success.style.display = 'block'; }
        } else { throw new Error(); }
      } catch {
        alert('Something went wrong. Please call us directly.');
        btn.disabled = false;
        btn.textContent = origText;
      }
    });
  }

  handleForm('enquiryForm',  'formSuccess');
  handleForm('contactForm',  'contactSuccess');
  handleForm('serviceForm',  'svcSuccess');

  /* ── Scroll Reveal (cards) ────────────────────────────────── */
  var revealEls = document.querySelectorAll('.product-card, .info-card, .testi-card, .ah-item');
  if ('IntersectionObserver' in window && revealEls.length) {
    revealEls.forEach(function (el, i) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = 'opacity .45s ease ' + (i % 5) * 80 + 'ms, transform .45s ease ' + (i % 5) * 80 + 'ms';
    });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    revealEls.forEach(function (el) { obs.observe(el); });
  }

})();

/* ============================================================
   ENQUIRY MODAL + EXPLORE SLIDER + PRODUCT DETAIL FORMS
   ============================================================ */

/* ── Open / Close Enquiry Modal ────────────────────────────── */
window.openEnquiryModal = function(name, img, price) {
  var modal = document.getElementById('enquiryModal');
  if (!modal) return;
  var titleEl = document.getElementById('modalProductTitle');
  var imgEl   = document.getElementById('modalProductImg');
  var priceEl = document.getElementById('modalProductPrice');
  var inputEl = document.getElementById('modalProductInput');
  if (titleEl) titleEl.textContent = name;
  if (imgEl)   { imgEl.src = img; imgEl.alt = name; }
  if (priceEl) priceEl.textContent = 'Price : ' + price;
  if (inputEl) inputEl.value = name;
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
};

function closeEnquiryModal() {
  var modal = document.getElementById('enquiryModal');
  if (modal) modal.style.display = 'none';
  document.body.style.overflow = '';
}

var modalCloseBtn = document.getElementById('modalClose');
if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeEnquiryModal);

var modalOverlay = document.getElementById('enquiryModal');
if (modalOverlay) {
  modalOverlay.addEventListener('click', function(e) {
    if (e.target === modalOverlay) closeEnquiryModal();
  });
}

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeEnquiryModal();
});

/* ── Modal Form Submit ─────────────────────────────────────── */
handleForm('modalForm', 'modalSuccess');

/* ── Product Detail Page Enquiry Form ──────────────────────── */
handleForm('pdEnquiryForm', 'pdEnqSuccess');

/* ── Explore More Slider ───────────────────────────────────── */
(function() {
  var track   = document.getElementById('exploreTrack');
  var prevBtn = document.getElementById('explorePrev');
  var nextBtn = document.getElementById('exploreNext');
  var dots    = document.querySelectorAll('.edot');
  if (!track) return;

  var cards     = track.querySelectorAll('.explore-card');
  var total     = cards.length;
  var perView   = window.innerWidth <= 600 ? 2 : 4;
  var current   = 0;
  var maxIdx    = Math.max(0, total - perView);

  function updateSlider() {
    var cardW  = cards[0] ? (cards[0].offsetWidth + 20) : 0;
    track.style.transform = 'translateX(-' + (current * cardW) + 'px)';
    track.style.transition = 'transform .4s ease';
    dots.forEach(function(d, i) { d.classList.toggle('active', i === current); });
  }

  if (prevBtn) prevBtn.addEventListener('click', function() {
    current = Math.max(0, current - 1); updateSlider();
  });
  if (nextBtn) nextBtn.addEventListener('click', function() {
    current = Math.min(maxIdx, current + 1); updateSlider();
  });
  dots.forEach(function(dot) {
    dot.addEventListener('click', function() {
      current = Math.min(parseInt(dot.dataset.idx), maxIdx);
      updateSlider();
    });
  });

  // Make track overflow visible for slide
  if (track.parentElement) {
    track.parentElement.style.overflow = 'hidden';
  }
  // Reset grid to flex for sliding
  track.style.display = 'flex';
  track.style.gap = '20px';
  cards.forEach(function(c) {
    c.style.minWidth = 'calc(25% - 15px)';
    if (window.innerWidth <= 600) c.style.minWidth = 'calc(50% - 10px)';
  });
})();



