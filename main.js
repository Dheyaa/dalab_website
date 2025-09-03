
// Mobile nav toggle
const nav = document.querySelector('.nav');
const btn = document.querySelector('.menu-btn');
if (btn) btn.addEventListener('click', () => nav.classList.toggle('open'));

// Reveal on scroll
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.2 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
