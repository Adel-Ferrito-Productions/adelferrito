// Main application initialization
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all animations and interactions
    if (typeof initAnimations === 'function') {
        initAnimations();
    }
    
    // Add error handling for missing images
    handleImageErrors();
    
    // Initialize performance monitoring
    initPerformanceMonitoring();
});

// Handle image loading errors gracefully
function handleImageErrors() {
    document.addEventListener('error', function(e) {
        if (e.target.tagName === 'IMG') {
            console.warn('Image failed to load:', e.target.src);
            
            // Replace with placeholder if it's a featured image
            if (e.target.src.includes('featured/')) {
                e.target.style.display = 'none';
                const placeholder = document.createElement('div');
                placeholder.className = 'placeholder-image';
                placeholder.innerHTML = `
                    <div>
                        <p>Image loading...</p>
                        <small>Please check your connection</small>
                    </div>
                `;
                e.target.parentNode.appendChild(placeholder);
            }
        }
    }, true);
}

// Basic performance monitoring
function initPerformanceMonitoring() {
    // Monitor page load performance
    window.addEventListener('load', function() {
        if ('performance' in window) {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
            }
        }
    });
    
    // Monitor image loading performance
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            // Image loaded successfully
        });
        
        img.addEventListener('error', function() {
            console.warn('Image failed to load:', this.src);
        });
    });
}

// Utility function to check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Utility function to debounce scroll events
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

// Export utility functions
window.isInViewport = isInViewport;
window.debounce = debounce; 