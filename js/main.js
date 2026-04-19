// Bulls Precision - Main Script
(function () {
    'use strict';

    // --- Navbar scroll effect ---
    const navbar = document.getElementById('navbar');
    const backToTop = document.getElementById('backToTop');
    // Product detail pages have a light hero; keep nav in solid/scrolled state
    // so link text stays readable regardless of scroll position.
    const alwaysSolid = !!document.querySelector('.product-hero');

    function onScroll() {
        const scrollY = window.scrollY;
        navbar.classList.toggle('scrolled', alwaysSolid || scrollY > 50);
        backToTop.classList.toggle('visible', scrollY > 500);

        // Update active nav link
        const sections = document.querySelectorAll('section[id]');
        sections.forEach(section => {
            const top = section.offsetTop - 120;
            const bottom = top + section.offsetHeight;
            const id = section.getAttribute('id');
            const link = document.querySelector(`.nav-links a[href="#${id}"]`);
            if (link) {
                link.classList.toggle('active', scrollY >= top && scrollY < bottom);
            }
        });
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // --- Mobile menu ---
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');

    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('open');
    });

    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            hamburger.classList.remove('open');
        });
    });

    // --- Back to top ---
    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // --- Counter animation ---
    function animateCounters() {
        const counters = document.querySelectorAll('[data-count]');
        counters.forEach(counter => {
            if (counter.dataset.animated) return;

            const rect = counter.getBoundingClientRect();
            if (rect.top > window.innerHeight || rect.bottom < 0) return;

            counter.dataset.animated = 'true';
            const target = parseInt(counter.dataset.count, 10);
            const duration = 2000;
            const start = performance.now();

            function update(now) {
                const elapsed = now - start;
                const progress = Math.min(elapsed / duration, 1);
                const ease = 1 - Math.pow(1 - progress, 3); // ease-out cubic
                counter.textContent = Math.floor(target * ease);
                if (progress < 1) {
                    requestAnimationFrame(update);
                } else {
                    counter.textContent = target;
                }
            }

            requestAnimationFrame(update);
        });
    }

    window.addEventListener('scroll', animateCounters, { passive: true });
    animateCounters();

    // --- Scroll reveal ---
    function revealElements() {
        // Tech cards
        document.querySelectorAll('.tech-card').forEach((card, i) => {
            const rect = card.getBoundingClientRect();
            if (rect.top < window.innerHeight - 80) {
                setTimeout(() => card.classList.add('visible'), i * 100);
            }
        });

        // Timeline items
        document.querySelectorAll('.timeline-item').forEach((item, i) => {
            const rect = item.getBoundingClientRect();
            if (rect.top < window.innerHeight - 60) {
                setTimeout(() => item.classList.add('visible'), i * 150);
            }
        });

        // Generic reveal
        document.querySelectorAll('.reveal').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight - 60) {
                el.classList.add('visible');
            }
        });
    }

    window.addEventListener('scroll', revealElements, { passive: true });
    revealElements();

    // --- Hero particles ---
    function createParticles() {
        const container = document.getElementById('particles');
        if (!container) return;

        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            const size = Math.random() * 4 + 2;
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.bottom = '-10px';
            particle.style.animationDuration = (Math.random() * 8 + 6) + 's';
            particle.style.animationDelay = (Math.random() * 10) + 's';
            container.appendChild(particle);
        }
    }

    createParticles();

    // --- Smooth scroll for anchor links ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                const offset = navbar.offsetHeight;
                const top = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });

    // --- Product detail: thumbnail gallery ---
    const thumbs = document.querySelectorAll('.product-image-thumbs .thumb');
    const mainImage = document.querySelector('.product-image-large img');
    if (thumbs.length && mainImage) {
        thumbs.forEach(thumb => {
            thumb.addEventListener('click', () => {
                const fullSrc = thumb.dataset.full;
                if (fullSrc) {
                    mainImage.src = fullSrc;
                }
                thumbs.forEach(t => t.classList.remove('active'));
                thumb.classList.add('active');
            });
        });
    }

    // --- Contact form ---
    const form = document.getElementById('contactForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const btn = form.querySelector('button[type="submit"]');
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Sending...</span>';
            btn.disabled = true;

            fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: { 'Accept': 'application/json' }
            }).then(res => {
                if (res.ok) {
                    btn.innerHTML = '<i class="fas fa-check"></i> <span>Submitted Successfully!</span>';
                    btn.style.background = '#10B981';
                    form.reset();
                } else {
                    btn.innerHTML = '<i class="fas fa-times"></i> <span>Failed, please try again</span>';
                    btn.style.background = '#EF4444';
                }
            }).catch(() => {
                btn.innerHTML = '<i class="fas fa-times"></i> <span>Network error, please try again</span>';
                btn.style.background = '#EF4444';
            }).finally(() => {
                setTimeout(() => {
                    btn.innerHTML = originalHTML;
                    btn.style.background = '';
                    btn.disabled = false;
                }, 3000);
            });
        });
    }
})();
