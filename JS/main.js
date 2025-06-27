// Main JavaScript for Adel Ferrito Photography Website
// Handles navigation, accessibility, animations, and enhanced functionality

// Global variables
let currentFontSize = 100; // percentage
let isHighContrast = false;
let isReducedMotion = false;

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeWebsite();
});

// Initialize all website functionality
function initializeWebsite() {
    setupNavigation();
    setupAccessibility();
    setupAnimations();
    setupKeyboardNavigation();
    setupPerformanceOptimizations();
    loadUserPreferences();
}

// Navigation functionality
function setupNavigation() {
    const navbar = document.getElementById('navbar');
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    // Smooth scroll for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                const navbarHeight = navbar.offsetHeight;
                const targetPosition = targetSection.offsetTop - navbarHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// Accessibility features
function setupAccessibility() {
    // Skip to content link
    const skipLink = document.createElement('a');
    skipLink.href = '#home';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'skip-link';
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Focus management
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-navigation');
    });
}

// Accessibility menu functions
function toggleAccessibilityMenu() {
    const menu = document.getElementById('accessibilityMenu');
    menu.classList.toggle('show');
}

function toggleHighContrast() {
    isHighContrast = !isHighContrast;
    document.body.classList.toggle('high-contrast', isHighContrast);
    saveUserPreferences();
    
    // Announce to screen readers
    announceToScreenReader(isHighContrast ? 'High contrast mode enabled' : 'High contrast mode disabled');
}

function increaseFontSize() {
    if (currentFontSize < 150) {
        currentFontSize += 10;
        document.documentElement.style.fontSize = currentFontSize + '%';
        saveUserPreferences();
        announceToScreenReader('Font size increased');
    }
}

function decreaseFontSize() {
    if (currentFontSize > 80) {
        currentFontSize -= 10;
        document.documentElement.style.fontSize = currentFontSize + '%';
        saveUserPreferences();
        announceToScreenReader('Font size decreased');
    }
}

function toggleReducedMotion() {
    isReducedMotion = !isReducedMotion;
    document.body.classList.toggle('reduced-motion', isReducedMotion);
    saveUserPreferences();
    
    announceToScreenReader(isReducedMotion ? 'Reduced motion enabled' : 'Reduced motion disabled');
}

// Animation setup
function setupAnimations() {
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
    
    // Observe all fade-in elements
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(el => observer.observe(el));
}

// Keyboard navigation
function setupKeyboardNavigation() {
    // Gallery navigation
    document.addEventListener('keydown', function(e) {
        const galleryModal = document.getElementById('galleryModal');
        const lightbox = document.getElementById('lightbox');
        
        if (e.key === 'Escape') {
            if (galleryModal.style.display === 'block') {
                closeGallery();
            }
            if (lightbox.style.display === 'block') {
                closeLightbox();
            }
        }
        
        // Arrow key navigation in galleries
        if (galleryModal.style.display === 'block') {
            const galleryImages = document.querySelectorAll('.gallery-image');
            const currentIndex = Array.from(galleryImages).findIndex(img => img === document.activeElement);
            
            if (e.key === 'ArrowRight' && currentIndex < galleryImages.length - 1) {
                galleryImages[currentIndex + 1].focus();
            } else if (e.key === 'ArrowLeft' && currentIndex > 0) {
                galleryImages[currentIndex - 1].focus();
            }
        }
    });
}

// Performance optimizations
function setupPerformanceOptimizations() {
    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        observer.unobserve(img);
                    }
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Preload critical resources
    preloadCriticalResources();
}

// Preload critical resources
function preloadCriticalResources() {
    const criticalImages = [
        'Assets/images/featured/malta-bw-hero_1200.webp',
        'Assets/images/featured/malta-bw-hero_1200.jpg'
    ];
    
    criticalImages.forEach(src => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'image';
        link.href = src;
        document.head.appendChild(link);
    });
}

// User preferences management
function saveUserPreferences() {
    const preferences = {
        fontSize: currentFontSize,
        highContrast: isHighContrast,
        reducedMotion: isReducedMotion
    };
    
    localStorage.setItem('adelFerritoPreferences', JSON.stringify(preferences));
}

function loadUserPreferences() {
    const saved = localStorage.getItem('adelFerritoPreferences');
    
    if (saved) {
        const preferences = JSON.parse(saved);
        currentFontSize = preferences.fontSize || 100;
        isHighContrast = preferences.highContrast || false;
        isReducedMotion = preferences.reducedMotion || false;
        
        // Apply saved preferences
        document.documentElement.style.fontSize = currentFontSize + '%';
        document.body.classList.toggle('high-contrast', isHighContrast);
        document.body.classList.toggle('reduced-motion', isReducedMotion);
    }
}

// Screen reader announcements
function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    // Remove after announcement
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Enhanced scroll handling
const handleScroll = debounce(function() {
    // Add any scroll-based functionality here
}, 16);

window.addEventListener('scroll', handleScroll);

// Error handling
window.addEventListener('error', function(e) {
    console.error('Website error:', e.error);
    // Could send to analytics service here
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
        }, 0);
    });
}

// Export functions for use in other scripts
window.toggleAccessibilityMenu = toggleAccessibilityMenu;
window.toggleHighContrast = toggleHighContrast;
window.increaseFontSize = increaseFontSize;
window.decreaseFontSize = decreaseFontSize;
window.toggleReducedMotion = toggleReducedMotion;

// Professional features
function openPrintInquiry(imageName, galleryTitle) {
    const subject = encodeURIComponent(`Print Inquiry: ${imageName} from ${galleryTitle}`);
    const body = encodeURIComponent(`Hello Adel,\n\nI'm interested in purchasing a print of "${imageName}" from your "${galleryTitle}" series.\n\nPlease let me know about:\n- Available sizes and prices\n- Paper options\n- Shipping information\n- Timeline for delivery\n\nThank you,\n[Your name]`);
    
    window.open(`mailto:ferritography@gmail.com?subject=${subject}&body=${body}`, '_blank');
}

function openCommissionInquiry(galleryTitle) {
    const subject = encodeURIComponent(`Commission Inquiry: ${galleryTitle} Style`);
    const body = encodeURIComponent(`Hello Adel,\n\nI'm interested in commissioning a piece in the style of your "${galleryTitle}" series.\n\nPlease let me know about:\n- Commission process and timeline\n- Pricing structure\n- Location requirements\n- Available formats and sizes\n\nThank you,\n[Your name]`);
    
    window.open(`mailto:ferritography@gmail.com?subject=${subject}&body=${body}`, '_blank');
}

// Export professional functions
window.openPrintInquiry = openPrintInquiry;
window.openCommissionInquiry = openCommissionInquiry; 