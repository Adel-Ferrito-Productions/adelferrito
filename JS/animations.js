// Navbar scroll effect
function initNavbarScroll() {
    window.addEventListener('scroll', function() {
        const navbar = document.getElementById('navbar');
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// Smooth scrolling for navigation
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Fade-in animation on scroll
function initFadeInAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });
}

// Preload featured images for better performance
function preloadFeaturedImages() {
    const featuredImages = [
        'assets/images/featured/storm-hero.jpg',
        'assets/images/featured/malta-bw-hero.jpg',
        'assets/images/featured/sicily-bw-hero.jpg'
    ];
    
    featuredImages.forEach(src => {
        const img = new Image();
        img.src = src;
    });
}

// Close modals with ESC key
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (typeof closeGallery === 'function') {
                closeGallery();
            }
            if (typeof closeLightbox === 'function') {
                closeLightbox();
            }
        }
    });
}

// Initialize all animations when DOM is loaded
function initAnimations() {
    initNavbarScroll();
    initSmoothScrolling();
    initFadeInAnimations();
    initKeyboardShortcuts();
    
    // Preload images after page load
    window.addEventListener('load', preloadFeaturedImages);
}

// Export initialization function
window.initAnimations = initAnimations; 