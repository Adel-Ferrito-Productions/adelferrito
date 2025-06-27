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

// Enhanced image metadata mapping for better ALT text and SEO
const imageMetadata = {
    'bw-malta': {
        '3 bodies copy': {
            title: 'Three Limestone Formations',
            description: 'Three dramatic limestone rock formations emerging from the Mediterranean Sea, captured in stark black and white contrast',
            location: 'Malta Coastline',
            keywords: 'limestone formations, Mediterranean rocks, black and white photography, Malta coastline, dramatic landscape'
        },
        'Buskette Tree BW': {
            title: 'Solitary Tree at Buskett',
            description: 'A lone tree standing majestically in the Buskett Gardens, its branches reaching skyward against a dramatic monochrome sky',
            location: 'Buskett Gardens, Malta',
            keywords: 'Buskett Gardens, solitary tree, black and white nature, Malta landscape, dramatic sky'
        },
        'Comino Rock 1 copy': {
            title: 'Comino Island Rock Formation',
            description: 'Dramatic rock formations on the shores of Comino Island, showcasing the island\'s rugged natural beauty in monochrome',
            location: 'Comino Island, Malta',
            keywords: 'Comino Island, rock formations, Malta islands, black and white landscape, Mediterranean geology'
        },
        'lady Gebla tal general copy': {
            title: 'Lady\'s Rock at General\'s Rock',
            description: 'The iconic Lady\'s Rock formation near General\'s Rock, a natural landmark of Malta\'s dramatic coastal landscape',
            location: 'General\'s Rock, Malta',
            keywords: 'Lady\'s Rock, General\'s Rock, Malta landmarks, coastal formations, black and white photography'
        },
        'Lapsi BW Filfla copy': {
            title: 'Lapsi View Towards Filfla',
            description: 'Panoramic view from Lapsi looking towards the distant island of Filfla, captured in dramatic black and white tones',
            location: 'Lapsi, Malta',
            keywords: 'Lapsi Malta, Filfla island, panoramic view, black and white landscape, Mediterranean vista'
        },
        'Mellieha-Cave-2020': {
            title: 'Mellieha Cave Interior',
            description: 'The mysterious interior of a cave in Mellieha, where natural light creates dramatic shadows and textures',
            location: 'Mellieha, Malta',
            keywords: 'Mellieha cave, cave photography, natural light, dramatic shadows, Malta geology'
        },
        'Mistiuqe---Swieqi-Jan-12-2022-www': {
            title: 'Mistique Building in Swieqi',
            description: 'The distinctive Mistique building in Swieqi, captured in black and white to emphasize its architectural lines and form',
            location: 'Swieqi, Malta',
            keywords: 'Mistique building, Swieqi Malta, architectural photography, black and white, modern architecture'
        },
        'Munxar sunrise copy': {
            title: 'Munxar Sunrise',
            description: 'The first light of dawn breaking over Munxar, creating a serene and peaceful morning atmosphere in monochrome',
            location: 'Munxar, Malta',
            keywords: 'Munxar sunrise, dawn photography, morning light, black and white landscape, Malta countryside'
        }
    },
    'bw-sicily': {
        'Caltabellotta-BW-Mountain': {
            title: 'Caltabellotta Mountain View',
            description: 'Dramatic mountain landscape surrounding the medieval village of Caltabellotta, captured in stark black and white contrast',
            location: 'Caltabellotta, Sicily',
            keywords: 'Caltabellotta mountain, Sicilian landscape, black and white photography, medieval village, dramatic terrain'
        },
        'Carta-Bellotta-2April-26,-2024Adel-Ferrito-copy': {
            title: 'Caltabellotta Street Scene',
            description: 'A quiet street in Caltabellotta village, showcasing the medieval architecture and timeless atmosphere',
            location: 'Caltabellotta, Sicily',
            keywords: 'Caltabellotta streets, medieval architecture, Sicilian village, black and white, timeless atmosphere'
        },
        'Selinunte-1-May-04-Adel-Ferrito-2024-copy': {
            title: 'Selinunte Temple Ruins',
            description: 'Ancient Greek temple ruins at Selinunte archaeological site, standing majestically against the Mediterranean sky',
            location: 'Selinunte Archaeological Park, Sicily',
            keywords: 'Selinunte ruins, Greek temples, archaeological photography, ancient Sicily, Mediterranean heritage'
        }
    },
    'storms': {
        '2-Golden-Bay-October-Storm-2-copy': {
            title: 'October Storm at Golden Bay',
            description: 'Dramatic storm clouds gathering over Golden Bay during October, creating an intense and atmospheric scene',
            location: 'Golden Bay, Malta',
            keywords: 'storm photography, Golden Bay Malta, dramatic weather, October storm, atmospheric photography'
        },
        '2-Golden-Bay-October-Storm-Print-NOV2022-copy': {
            title: 'Storm Over Golden Bay',
            description: 'Powerful storm system moving across Golden Bay, captured in dramatic black and white to emphasize the storm\'s intensity',
            location: 'Golden Bay, Malta',
            keywords: 'storm photography, Golden Bay, dramatic weather, black and white storm, Malta weather'
        }
    },
    'golden-hour': {
        '01.06.2020--Sunset-Pano-Riviera-2024-edit': {
            title: 'Sunset Panorama at Riviera',
            description: 'Breathtaking sunset panorama over the Riviera coastline, with golden light painting the Mediterranean waters',
            location: 'Riviera, Malta',
            keywords: 'sunset photography, Riviera Malta, golden hour, Mediterranean sunset, panoramic landscape'
        }
    },
    'dramatic-architecture': {
        'bench uppe barrakka copy': {
            title: 'Bench at Upper Barrakka Gardens',
            description: 'A solitary bench in the Upper Barrakka Gardens, overlooking the Grand Harbor with dramatic architectural backdrop',
            location: 'Upper Barrakka Gardens, Valletta, Malta',
            keywords: 'Upper Barrakka Gardens, Valletta architecture, Grand Harbor view, dramatic architecture, Malta landmarks'
        }
    },
    'landscapes': {
        'cartabellotta-Church-Wide-April-26,-2024Adel-Ferrito-copy': {
            title: 'Caltabellotta Church Wide View',
            description: 'Wide-angle view of the church in Caltabellotta village, showcasing the medieval architecture against the Sicilian landscape',
            location: 'Caltabellotta, Sicily',
            keywords: 'Caltabellotta church, Sicilian architecture, medieval church, wide-angle photography, village landscape'
        }
    },
    'salinunte': {
        'Selinunte-1-May-04-Adel-Ferrito-2024-copy': {
            title: 'Selinunte Temple E',
            description: 'Temple E at the Selinunte archaeological site, one of the best-preserved Greek temples in Sicily',
            location: 'Selinunte Archaeological Park, Sicily',
            keywords: 'Selinunte Temple E, Greek archaeology, Sicilian ruins, ancient temples, Mediterranean heritage'
        },
        'Selinunte-1-May-05-Adel-Ferrito-2024-copy': {
            title: 'Selinunte Temple Complex',
            description: 'The majestic temple complex at Selinunte, showcasing the grandeur of ancient Greek architecture in Sicily',
            location: 'Selinunte Archaeological Park, Sicily',
            keywords: 'Selinunte temples, Greek architecture, archaeological site, Sicilian heritage, ancient ruins'
        }
    },
    'caltabellotta': {
        'Caltabellotta-BW-Mountain': {
            title: 'Caltabellotta Mountain Village',
            description: 'The medieval village of Caltabellotta perched dramatically on the mountainside, captured in monochrome',
            location: 'Caltabellotta, Sicily',
            keywords: 'Caltabellotta village, medieval Sicily, mountain village, black and white photography, dramatic landscape'
        }
    },
    'grotte': {
        'Renato-May-01,-2024Adel-Ferrito-copy': {
            title: 'Cave Interior - Natural Light',
            description: 'The interior of a natural cave where sunlight creates dramatic light shafts and reveals the cave\'s hidden beauty',
            location: 'Malta',
            keywords: 'cave photography, natural light, cave interior, dramatic lighting, Malta geology'
        }
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

// Enhanced ALT text generation with SEO optimization
function generateAltText(filename, gallery) {
    const baseName = filename.replace(/\.[^/.]+$/, ''); // Remove extension
    
    // Check if we have specific metadata for this image
    const galleryMetadata = imageMetadata[gallery.folder];
    if (galleryMetadata && galleryMetadata[baseName]) {
        const metadata = galleryMetadata[baseName];
        return `${metadata.title} - ${metadata.description} - Fine art photography by Adel Ferrito. ${metadata.keywords}`;
    }
    
    // Fallback: Generate from filename with context
    const formattedName = baseName
        .replace(/[-_]/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase())
        .replace(/Copy/g, '')
        .replace(/\s+/g, ' ')
        .trim();
    
    // Add location context based on gallery
    let location = '';
    switch(gallery.folder) {
        case 'bw-malta':
            location = 'Malta';
            break;
        case 'bw-sicily':
            location = 'Sicily';
            break;
        case 'storms':
            location = 'Mediterranean';
            break;
        case 'golden-hour':
            location = 'Mediterranean';
            break;
        case 'dramatic-architecture':
            location = 'Malta & Sicily';
            break;
        case 'landscapes':
            location = 'Mediterranean';
            break;
        case 'salinunte':
            location = 'Selinunte, Sicily';
            break;
        case 'caltabellotta':
            location = 'Caltabellotta, Sicily';
            break;
        case 'grotte':
            location = 'Malta & Sicily';
            break;
        default:
            location = 'Mediterranean';
    }
    
    return `${formattedName} - ${gallery.title} - Fine art photography by Adel Ferrito. Location: ${location}. ${gallery.description}`;
}

// Enhanced image title generation
function formatImageTitle(filename) {
    const baseName = filename.replace(/\.[^/.]+$/, '');
    
    // Check for specific metadata first
    for (const galleryKey in imageMetadata) {
        const galleryMetadata = imageMetadata[galleryKey];
        if (galleryMetadata[baseName]) {
            return galleryMetadata[baseName].title;
        }
    }
    
    // Fallback: Generate from filename
    return baseName
        .replace(/[-_]/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase())
        .replace(/Copy/g, '')
        .replace(/\s+/g, ' ')
        .trim();
}

// Generate SEO-optimized image description
function generateImageDescription(filename, gallery) {
    const baseName = filename.replace(/\.[^/.]+$/, '');
    
    // Check for specific metadata
    const galleryMetadata = imageMetadata[gallery.folder];
    if (galleryMetadata && galleryMetadata[baseName]) {
        const metadata = galleryMetadata[baseName];
        return `${metadata.description} - ${metadata.location} - Fine art photography by Adel Ferrito. Keywords: ${metadata.keywords}`;
    }
    
    // Fallback description
    return `${formatImageTitle(filename)} - ${gallery.description} - Fine art photography by Adel Ferrito. Location: ${gallery.location}`;
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
        imageElement.setAttribute('aria-label', `View ${formatImageTitle(image.original)} in lightbox`);
        
        // Generate enhanced alt text
        const altText = generateAltText(image.original, gallery);
        
        const optimizedSources = getOptimizedImageSources(image.original, gallery.folder);
        
        imageElement.innerHTML = `
            <picture>
                <source srcset="${optimizedSources.webpSrcset}" type="image/webp" sizes="${optimizedSources.sizes}">
                <img src="Assets/images/${gallery.folder}/${image.original}" 
                     srcset="${optimizedSources.srcset}"
                     sizes="${optimizedSources.sizes}"
                     alt="${altText}"
                     loading="lazy"
                     title="${formatImageTitle(image.original)}">
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
    lightboxImage.title = formatImageTitle(image.original);
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