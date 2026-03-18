// ═══════════════════════════════════════════════════
//  MAIN — Preloader, Noise, Cursor, GSAP, ScrollTrigger
// ═══════════════════════════════════════════════════

gsap.registerPlugin(ScrollTrigger);

// ── Film-grain noise canvas ──────────────────────────
(function noiseCanvas() {
  const c   = document.getElementById('noise-canvas');
  if (!c) return;
  const ctx = c.getContext('2d');
  let W, H, frame;

  function resize() {
    W = c.width  = window.innerWidth;
    H = c.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  function drawNoise() {
    const img = ctx.createImageData(W, H);
    const d   = img.data;
    for (let i = 0; i < d.length; i += 4) {
      const v = (Math.random() * 255) | 0;
      d[i] = d[i+1] = d[i+2] = v;
      d[i+3] = 255;
    }
    ctx.putImageData(img, 0, 0);
    frame = requestAnimationFrame(drawNoise);
  }
  drawNoise();
})();

// ── Lenis smooth scroll ──────────────────────────────
const lenis = new Lenis({ lerp: 0.1, smooth: true });
function raf(t) { lenis.raf(t); requestAnimationFrame(raf); }
requestAnimationFrame(raf);
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add(t => lenis.raf(t * 1000));
gsap.ticker.lagSmoothing(0);

// ── Preloader ────────────────────────────────────────
(function preloader() {
  const el    = document.getElementById('preloader');
  const count = document.getElementById('pre-count');
  const line  = document.querySelector('.pre-line');
  if (!el) return;

  let progress = 0;
  const interval = setInterval(() => {
    progress += Math.random() * 18;
    if (progress >= 100) {
      progress = 100;
      clearInterval(interval);
      setTimeout(finish, 300);
    }
    count.textContent = Math.floor(progress);
    line.style.width  = progress + '%';
  }, 80);

  function finish() {
    el.classList.add('done');
    document.body.classList.remove('loading');
    // entrance animations after preloader
    heroEntrance();
  }
})();

// ── Hero entrance animations ─────────────────────────
function heroEntrance() {
  gsap.fromTo('.hero-meta', { opacity: 0, y: 12 }, {
    opacity: 1, y: 0, stagger: 0.08, duration: 0.8,
    ease: 'power3.out', delay: 0.2
  });
  gsap.fromTo('.hl-word', { yPercent: 110 }, {
    yPercent: 0, stagger: 0.18, duration: 1.1,
    ease: 'power4.out', delay: 0.3
  });
  gsap.fromTo('#hero-portrait-wrap', { opacity: 0, x: 40 }, {
    opacity: 1, x: 0, duration: 1.4, ease: 'power4.out', delay: 0.5
  });
  gsap.fromTo('.hero-role-belt', { opacity: 0 }, {
    opacity: 1, duration: 0.8, delay: 0.9
  });
}

// ── Custom cursor ────────────────────────────────────
(function cursor() {
  const cur = document.getElementById('cursor');
  if (!cur) return;

  let cx = 0, cy = 0;
  window.addEventListener('mousemove', e => {
    gsap.to(cur, { x: e.clientX, y: e.clientY, duration: 0.55, ease: 'power3.out' });
    cx = e.clientX; cy = e.clientY;
  });

  // Hover states
  document.querySelectorAll('a, button, .work-item').forEach(el => {
    el.addEventListener('mouseenter', () => cur.classList.add('cursor-hover'));
    el.addEventListener('mouseleave', () => {
      cur.classList.remove('cursor-hover');
      cur.classList.remove('cursor-work');
      document.getElementById('cur-label').textContent = '';
    });
  });
  document.querySelectorAll('.work-item').forEach(el => {
    el.addEventListener('mouseenter', () => {
      cur.classList.add('cursor-work');
      document.getElementById('cur-label').textContent = 'VIEW';
    });
  });
})();

// ── Nav menu ─────────────────────────────────────────
const menuBtn  = document.getElementById('nav-menu-btn');
const fullMenu = document.getElementById('fullmenu');
let menuOpen   = false;

function toggleMenu() {
  menuOpen = !menuOpen;
  menuBtn.classList.toggle('open', menuOpen);
  fullMenu.classList.toggle('open', menuOpen);
  lenis[ menuOpen ? 'stop' : 'start' ]();

  if (menuOpen) {
    gsap.fromTo('.fm-link', { yPercent: 80, opacity: 0 }, {
      yPercent: 0, opacity: 0.25, stagger: 0.06,
      duration: 0.7, ease: 'power3.out', delay: 0.35
    });
  }
}
menuBtn.addEventListener('click', toggleMenu);
document.querySelectorAll('.fm-link').forEach(l => l.addEventListener('click', toggleMenu));

// ── About — statement text reveal ────────────────────
gsap.fromTo('.st-line', { yPercent: 105 }, {
  yPercent: 0, stagger: 0.1, duration: 1.0, ease: 'power4.out',
  scrollTrigger: { trigger: '#about', start: 'top 75%' }
});
gsap.fromTo('#st-label', { opacity: 0, x: -20 }, {
  opacity: 1, x: 0, duration: 0.7, ease: 'power3.out',
  scrollTrigger: { trigger: '#about', start: 'top 80%' }
});
gsap.fromTo('#st-sub', { opacity: 0, y: 30 }, {
  opacity: 1, y: 0, duration: 0.9, ease: 'power3.out',
  scrollTrigger: { trigger: '.statement-sub', start: 'top 85%' }
});
gsap.fromTo('.ss-item', { opacity: 0, y: 20 }, {
  opacity: 1, y: 0, stagger: 0.12, duration: 0.6, ease: 'power3.out',
  scrollTrigger: { trigger: '.statement-stats', start: 'top 88%' }
});

// ── Work section ─────────────────────────────────────
gsap.fromTo('#work-header', { opacity: 0, y: 40 }, {
  opacity: 1, y: 0, duration: 0.9, ease: 'power3.out',
  scrollTrigger: { trigger: '#work', start: 'top 80%' }
});
gsap.fromTo('.work-item', { opacity: 0, y: 50 }, {
  opacity: 1, y: 0, stagger: 0.12, duration: 0.8, ease: 'power3.out',
  scrollTrigger: { trigger: '.work-list', start: 'top 85%' }
});

// ── Skills — animate rows + lines ────────────────────
gsap.fromTo('#skills-left', { opacity: 0, x: -40 }, {
  opacity: 1, x: 0, duration: 1.0, ease: 'power3.out',
  scrollTrigger: { trigger: '#skills', start: 'top 75%' }
});

// Animate skill tags
gsap.fromTo('.skill-tags span', { opacity: 0, y: 20 }, {
  opacity: 1, y: 0,
  stagger: 0.06, duration: 0.6, ease: 'power3.out',
  scrollTrigger: {
    trigger: '#skills', start: 'top 75%'
  }
});

// ── Contact section reveal ────────────────────────────
gsap.fromTo('#c-label', { opacity: 0, x: -20 }, {
  opacity: 1, x: 0, duration: 0.7, ease: 'power3.out',
  scrollTrigger: { trigger: '#contact', start: 'top 80%' }
});
gsap.fromTo('#contact-cta', { opacity: 0, y: 60 }, {
  opacity: 1, y: 0, duration: 1.1, ease: 'power4.out',
  scrollTrigger: { trigger: '#contact', start: 'top 75%' }
});
gsap.fromTo('#contact-footer', { opacity: 0 }, {
  opacity: 1, duration: 0.8,
  scrollTrigger: { trigger: '#contact-footer', start: 'top 90%' }
});

// ── Hero parallax on scroll ──────────────────────────
gsap.to('.hero-headline-wrap', {
  yPercent: -20, ease: 'none',
  scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom top', scrub: 1 }
});
gsap.to('#hero-portrait-wrap', {
  yPercent: 15, ease: 'none',
  scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom top', scrub: 1.5 }
});
gsap.to('.hero-role-belt', {
  opacity: 0, ease: 'none',
  scrollTrigger: { trigger: '#hero', start: '30% top', end: '60% top', scrub: 1 }
});
