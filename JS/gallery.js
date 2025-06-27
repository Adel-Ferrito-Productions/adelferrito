// Gallery configurations with SEO-optimized content and responsive image support
const galleries = {
    'storms': {
        title: 'Storm Studies',
        description: 'Mediterranean thunderstorms captured with dramatic intensity, showcasing the raw power and sublime beauty of nature\'s most spectacular displays.',
        seoTitle: 'Storm Photography Malta Sicily - Lightning and Dramatic Weather',
        folder: 'storms',
        category: 'Nature',
        year: '2024',
        location: 'Malta & Sicily',
        featured: true,
        exhibitions: ['Mediterranean Light Exhibition, Valletta 2024'],
        prints: true,
        commissions: true
    },
    'malta-bw': {
        title: 'Malta: Black & White',
        description: 'Timeless monochrome studies of Malta\'s dramatic landscapes, ancient architecture, and Mediterranean character rendered in fine art black and white.',
        seoTitle: 'Malta Black and White Photography - Fine Art Monochrome Landscapes',
        folder: 'bw-malta',
        category: 'Architecture',
        year: '2024',
        location: 'Malta',
        featured: true,
        exhibitions: ['Monochrome Malta, Sliema Gallery 2024'],
        prints: true,
        commissions: true
    },
    'sicily-bw': {
        title: 'Sicily: Echoes of Time',
        description: 'A meditation on Sicily\'s layered history through black and white photography, from ancient Greek ruins to medieval hilltop villages.',
        seoTitle: 'Sicily Black and White Photography - Ancient Ruins and Medieval Towns',
        folder: 'bw-sicily',
        category: 'Architecture',
        year: '2024',
        location: 'Sicily',
        featured: true,
        exhibitions: ['Ancient Echoes, Palermo Contemporary 2024'],
        prints: true,
        commissions: true
    },
    'golden-hour': {
        title: 'Golden Hour',
        description: 'The transformative quality of Mediterranean light during sunrise and sunset, capturing the poetry of changing illumination.',
        seoTitle: 'Golden Hour Photography Malta Sicily - Sunrise and Sunset Fine Art',
        folder: 'golden-hour',
        category: 'Landscape',
        year: '2024',
        location: 'Malta & Sicily',
        featured: false,
        exhibitions: [],
        prints: true,
        commissions: true
    },
    'architecture': {
        title: 'Architectural Studies',
        description: 'The dialogue between light, form, and space in Mediterranean architecture, from ancient temples to contemporary design.',
        seoTitle: 'Architectural Photography Malta Sicily - Ancient and Modern Buildings',
        folder: 'dramatic-architecture',
        category: 'Architecture',
        year: '2024',
        location: 'Malta & Sicily',
        featured: false,
        exhibitions: ['Mediterranean Architecture, Valletta Design Week 2024'],
        prints: true,
        commissions: true
    },
    'landscapes': {
        title: 'Mediterranean Landscapes',
        description: 'The diverse terrains and coastal beauty of Malta and Sicily captured through an artistic lens, revealing hidden poetry in familiar places.',
        seoTitle: 'Mediterranean Landscape Photography - Malta and Sicily Fine Art',
        folder: 'landscapes',
        category: 'Landscape',
        year: '2024',
        location: 'Malta & Sicily',
        featured: false,
        exhibitions: [],
        prints: true,
        commissions: true
    },
    'salinunte': {
        title: 'Selinunte',
        description: 'Ancient Greek ruins where history and landscape converge in timeless composition, capturing the dialogue between past and present.',
        seoTitle: 'Selinunte Archaeological Photography - Ancient Greek Ruins Sicily',
        folder: 'salinunte',
        category: 'Archaeology',
        year: '2024',
        location: 'Sicily',
        featured: false,
        exhibitions: ['Archaeological Perspectives, Catania Museum 2024'],
        prints: true,
        commissions: true
    },
    'caltabellotta': {
        title: 'Caltabellotta',
        description: 'A medieval Sicilian village perched between earth and sky, captured in monochrome poetry that speaks of centuries and silence.',
        seoTitle: 'Caltabellotta Photography - Medieval Sicilian Village Black and White',
        folder: 'caltabellotta',
        category: 'Architecture',
        year: '2024',
        location: 'Sicily',
        featured: false,
        exhibitions: [],
        prints: true,
        commissions: true
    },
    'caves': {
        title: 'Hidden Grottos',
        description: 'The secret chambers and coastal caves where light becomes sculpture, revealing nature\'s hidden architecture beneath the surface.',
        seoTitle: 'Cave Photography Malta Sicily - Hidden Grottos and Coastal Caves',
        folder: 'grotte',
        category: 'Nature',
        year: '2024',
        location: 'Malta & Sicily',
        featured: false,
        exhibitions: ['Natural Architecture, Gozo Contemporary 2024'],
        prints: true,
        commissions: true
    }
};

// Load optimized image mapping
let imageMapping = [];

// Load the image mapping from the generated JSON file
async function loadImageMapping() {
    try {
        const response = await fetch('Assets/images/galleries.json');
        imageMapping = await response.json();
    } catch (error) {
        console.warn('Could not load image mapping, falling back to static gallery data');
    }
}

// Get optimized image sources for a given original image
function getOptimizedImageSources(originalImage, folder) {
    const mapping = imageMapping.find(img => 
        img.original === originalImage && 
        img.folder.includes(folder)
    );
    
    if (!mapping) {
        // Fallback to original image if mapping not found
        return {
            srcset: `Assets/images/${folder}/${originalImage}`,
            webpSrcset: `Assets/images/${folder}/${originalImage}`,
            sizes: '(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw'
        };
    }
    
    const jpgSrcset = mapping.sizes.map(size => 
        `Assets/images/${folder}/${size.jpg} ${size.label.replace('px', 'w')}`
    ).join(', ');
    
    const webpSrcset = mapping.sizes.map(size => 
        `Assets/images/${folder}/${size.webp} ${size.label.replace('px', 'w')}`
    ).join(', ');
    
    return {
        srcset: jpgSrcset,
        webpSrcset: webpSrcset,
        sizes: '(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw'
    };
}

// Gallery functions
function openGallery(galleryKey) {
    const gallery = galleries[galleryKey];
    if (!gallery) return;

    // Update page title for SEO
    document.title = `${gallery.seoTitle} - Adel Ferrito Photography`;
    
    // Update meta description
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
        metaDesc.content = gallery.description;
    }

    // Populate gallery modal
    document.getElementById('galleryTitle').textContent = gallery.title;
    document.getElementById('galleryDescription').textContent = gallery.description;
    
    const galleryGrid = document.getElementById('galleryGrid');
    galleryGrid.innerHTML = '';
    
    // Get images for this gallery from the mapping
    const galleryImages = imageMapping.filter(img => 
        img.folder.includes(gallery.folder)
    );
    
    galleryImages.forEach((image, index) => {
        const imageElement = document.createElement('div');
        imageElement.className = 'gallery-image';
        imageElement.setAttribute('tabindex', '0');
        imageElement.setAttribute('role', 'button');
        imageElement.setAttribute('aria-label', `View ${image.original} in lightbox`);
        
        // Generate alt text from filename
        const altText = generateAltText(image.original, gallery);
        
        const optimizedSources = getOptimizedImageSources(image.original, gallery.folder);
        
        imageElement.innerHTML = `
            <picture>
                <source srcset="${optimizedSources.webpSrcset}" type="image/webp" sizes="${optimizedSources.sizes}">
                <img src="Assets/images/${gallery.folder}/${image.original}" 
                     srcset="${optimizedSources.srcset}"
                     sizes="${optimizedSources.sizes}"
                     alt="${altText}"
                     loading="lazy">
            </picture>
            <div class="image-info">
                <div class="image-title">${formatImageTitle(image.original)}</div>
                <div class="image-details">${gallery.location}, ${gallery.year}</div>
                <div class="image-actions">
                    ${gallery.prints ? '<button class="btn-print" onclick="event.stopPropagation(); openPrintInquiry(\'' + image.original + '\', \'' + gallery.title + '\')">Buy Print</button>' : ''}
                    ${gallery.commissions ? '<button class="btn-commission" onclick="event.stopPropagation(); openCommissionInquiry(\'' + gallery.title + '\')">Commission</button>' : ''}
                </div>
            </div>
        `;
        
        // Add click and keyboard event listeners
        imageElement.addEventListener('click', () => openLightbox(image, gallery, optimizedSources));
        imageElement.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openLightbox(image, gallery, optimizedSources);
            }
        });
        
        galleryGrid.appendChild(imageElement);
    });
    
    document.getElementById('galleryModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // Focus management for accessibility
    const firstImage = galleryGrid.querySelector('.gallery-image');
    if (firstImage) firstImage.focus();
}

function closeGallery() {
    document.getElementById('galleryModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    
    // Reset page title
    document.title = 'Adel Ferrito - Fine Art Photography';
    
    // Reset meta description
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
        metaDesc.content = 'Fine art photography by Adel Ferrito. Storm photography, black and white landscapes, and architectural studies from Malta and Sicily. Gallery exhibitions and commissioned work available.';
    }
}

function openLightbox(image, gallery, optimizedSources) {
    const lightbox = document.getElementById('lightbox');
    const lightboxImage = document.getElementById('lightboxImage');
    
    // Use the largest available size for lightbox
    const largestSize = image.sizes[image.sizes.length - 1];
    const lightboxSrc = `Assets/images/${gallery.folder}/${largestSize.webp}`;
    
    lightboxImage.src = lightboxSrc;
    lightboxImage.alt = generateAltText(image.original, gallery);
    lightbox.style.display = 'block';
    
    // Add lightbox actions
    const lightboxActions = document.createElement('div');
    lightboxActions.className = 'lightbox-actions';
    lightboxActions.innerHTML = `
        ${gallery.prints ? '<button class="btn-print" onclick="openPrintInquiry(\'' + image.original + '\', \'' + gallery.title + '\')">Buy Print</button>' : ''}
        ${gallery.commissions ? '<button class="btn-commission" onclick="openCommissionInquiry(\'' + gallery.title + '\')">Commission</button>' : ''}
        <button class="btn-close" onclick="closeLightbox()">Close</button>
    `;
    
    // Remove existing actions if any
    const existingActions = lightbox.querySelector('.lightbox-actions');
    if (existingActions) existingActions.remove();
    
    lightbox.appendChild(lightboxActions);
}

function closeLightbox() {
    document.getElementById('lightbox').style.display = 'none';
}

// Utility functions
function generateAltText(filename, gallery) {
    const baseName = filename.replace(/\.[^/.]+$/, ''); // Remove extension
    const formattedName = baseName.replace(/[-_]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    return `${formattedName} - ${gallery.title} - Fine art photography by Adel Ferrito`;
}

function formatImageTitle(filename) {
    const baseName = filename.replace(/\.[^/.]+$/, '');
    return baseName.replace(/[-_]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

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

// Initialize gallery system
document.addEventListener('DOMContentLoaded', () => {
    loadImageMapping();
    
    // Add keyboard navigation for gallery modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (document.getElementById('galleryModal').style.display === 'block') {
                closeGallery();
            }
            if (document.getElementById('lightbox').style.display === 'block') {
                closeLightbox();
            }
        }
    });
}); 