// Gallery configurations with SEO-optimized content and responsive image support
const galleries = {
    'storms': {
        title: 'Storm Studies',
        description: 'Dramatic Mediterranean thunderstorms captured in their most powerful moments',
        folder: 'storms',
        location: 'Malta & Sicily',
        year: '2019-2024',
        prints: false,
        commissions: true,
        seoTitle: 'Storm Photography Collection - Adel Ferrito'
    },
    'bw-malta': {
        title: 'Malta: Black & White',
        description: 'Timeless monochrome studies of Malta\'s dramatic landscapes and architecture',
        folder: 'bw-malta',
        location: 'Malta',
        year: '2020-2024',
        prints: false,
        commissions: true,
        seoTitle: 'Black & White Malta Photography - Adel Ferrito'
    },
    'bw-sicily': {
        title: 'Sicily: Echoes of Time',
        description: 'Ancient ruins and medieval villages captured in stark black and white',
        folder: 'bw-sicily',
        location: 'Sicily',
        year: '2024',
        prints: false,
        commissions: true,
        seoTitle: 'Black & White Sicily Photography - Adel Ferrito'
    },
    'sicily-bw': {
        title: 'Sicily: Echoes of Time',
        description: 'Ancient ruins and medieval villages captured in stark black and white',
        folder: 'bw-sicily',
        location: 'Sicily',
        year: '2024',
        prints: false,
        commissions: true,
        seoTitle: 'Black & White Sicily Photography - Adel Ferrito'
    },
    'gibellina-bw': {
        title: 'Gibellina: Black & White',
        description: 'The reconstructed city of Gibellina captured in dramatic monochrome',
        folder: 'landscapes',
        location: 'Gibellina, Sicily',
        year: '2024',
        prints: false,
        commissions: true,
        seoTitle: 'Gibellina Black & White Photography - Adel Ferrito',
        filter: 'Gibellina' // Special filter for Gibellina images
    },
    'caltabellotta-giosamaria': {
        title: 'Caltabellotta & Giosamaria',
        description: 'Medieval Sicilian villages and landscapes in black and white',
        folder: 'caltabellotta',
        location: 'Caltabellotta & Giosamaria, Sicily',
        year: '2024',
        prints: false,
        commissions: true,
        seoTitle: 'Caltabellotta Giosamaria Photography - Adel Ferrito'
    },
    'architecture-malta-bw': {
        title: 'Malta: Architectural Studies',
        description: 'Black and white architectural studies of Malta\'s historic buildings and structures',
        folder: 'dramatic-architecture',
        location: 'Malta',
        year: '2020-2024',
        prints: false,
        commissions: true,
        seoTitle: 'Malta Architectural Photography - Adel Ferrito'
    },
    'golden-hour': {
        title: 'Golden Hour',
        description: 'Sunrise and sunset studies capturing the transformative quality of Mediterranean light',
        folder: 'golden-hour',
        location: 'Malta & Sicily',
        year: '2020-2024',
        prints: false,
        commissions: true,
        seoTitle: 'Golden Hour Photography - Adel Ferrito'
    },
    'landscapes': {
        title: 'Mediterranean Landscapes',
        description: 'The diverse terrains and coastal beauty of Malta and Sicily through an artistic lens',
        folder: 'landscapes',
        location: 'Malta & Sicily',
        year: '2020-2024',
        prints: false,
        commissions: true,
        seoTitle: 'Mediterranean Landscape Photography - Adel Ferrito',
        exclude: ['Gibellina', 'Gioiosa'] // Exclude these from main landscapes gallery
    },
    'salinunte': {
        title: 'Selinunte',
        description: 'Ancient Greek ruins where history and landscape converge in timeless composition',
        folder: 'salinunte',
        location: 'Selinunte, Sicily',
        year: '2024',
        prints: false,
        commissions: true,
        seoTitle: 'Selinunte Archaeological Photography - Adel Ferrito'
    },
    'caves': {
        title: 'Hidden Grottos',
        description: 'The secret chambers and coastal caves where light becomes sculpture',
        folder: 'grotte',
        location: 'Malta & Sicily',
        year: '2024',
        prints: false,
        commissions: true,
        seoTitle: 'Cave and Grotto Photography - Adel Ferrito'
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
    'landscapes': {
        'Gibellina-10-DAY-3-April-30,-2024Adel-Ferrito-copy': {
            title: 'Gibellina Reconstruction',
            description: 'The reconstructed city of Gibellina showcasing modern architecture and urban planning in dramatic black and white',
            location: 'Gibellina, Sicily',
            keywords: 'Gibellina reconstruction, modern architecture, Sicilian city, black and white photography, urban landscape'
        },
        'Gibellina-11-DAY-3-April-30,-2024Adel-Ferrito-copy': {
            title: 'Gibellina Urban Landscape',
            description: 'Urban landscape of the reconstructed city of Gibellina captured in stark monochrome',
            location: 'Gibellina, Sicily',
            keywords: 'Gibellina urban, modern Sicilian city, black and white photography, reconstruction, urban planning'
        },
        'Gibellina-12-DAY-3-April-30,-2024Adel-Ferrito-copy': {
            title: 'Gibellina Architecture',
            description: 'Modern architectural elements of Gibellina city captured in dramatic black and white',
            location: 'Gibellina, Sicily',
            keywords: 'Gibellina architecture, modern buildings, Sicilian reconstruction, black and white, contemporary design'
        },
        'Day-1---Gioiosa-MareaJune-04,-2024-Adel-Ferrito-copy': {
            title: 'Gioiosa Marea Coastline',
            description: 'The dramatic coastline of Gioiosa Marea captured in black and white',
            location: 'Gioiosa Marea, Sicily',
            keywords: 'Gioiosa Marea, Sicilian coastline, black and white photography, Mediterranean coast, dramatic landscape'
        },
        'Day-1---Gioiosa-MareaJune-13,-2024-Adel-Ferrito-copy': {
            title: 'Gioiosa Marea Village',
            description: 'The charming village of Gioiosa Marea in dramatic monochrome',
            location: 'Gioiosa Marea, Sicily',
            keywords: 'Gioiosa Marea village, Sicilian town, black and white photography, Mediterranean village, traditional architecture'
        },
        'Day-1---Gioiosa-MareaJune-14,-2024-Adel-Ferrito-copy': {
            title: 'Gioiosa Marea Landscape',
            description: 'Landscape view of Gioiosa Marea showcasing the village and surrounding countryside',
            location: 'Gioiosa Marea, Sicily',
            keywords: 'Gioiosa Marea landscape, Sicilian countryside, black and white photography, village life, rural Sicily'
        }
    },
    'storms': {
        'Valletta 1 copy': {
            title: 'Storm Over Valletta',
            description: 'Dramatic storm clouds gathering over the historic city of Valletta, creating an intense atmospheric scene',
            location: 'Valletta, Malta',
            keywords: 'storm photography, Valletta Malta, dramatic weather, atmospheric photography, Mediterranean storms'
        },
        'Valletta 3 copy': {
            title: 'Lightning Over Valletta',
            description: 'Electric lightning illuminating the night sky over Valletta\'s historic fortifications',
            location: 'Valletta, Malta',
            keywords: 'lightning photography, Valletta Malta, dramatic weather, night photography, storm lightning'
        },
        'Valletta 5 copy': {
            title: 'Storm Front Approaching Valletta',
            description: 'A powerful storm front moving towards Valletta, captured in dramatic black and white',
            location: 'Valletta, Malta',
            keywords: 'storm front, Valletta Malta, dramatic weather, approaching storm, atmospheric photography'
        },
        'Thunder Tarxien copy': {
            title: 'Thunderstorm at Tarxien',
            description: 'Intense thunderstorm activity over Tarxien, with dramatic cloud formations and atmospheric lighting',
            location: 'Tarxien, Malta',
            keywords: 'thunderstorm, Tarxien Malta, dramatic weather, lightning photography, storm clouds'
        },
        'Zurrieq-Sep-2020-1st-strom-copy': {
            title: 'First Storm of September 2020',
            description: 'The inaugural storm of September 2020 over Zurrieq, marking the beginning of the storm season',
            location: 'Zurrieq, Malta',
            keywords: 'September storm, Zurrieq Malta, 2020 storms, dramatic weather, seasonal storms'
        },
        'September-2021-Church-Dingly-2-copy': {
            title: 'Storm Over Dingli Church',
            description: 'Dramatic storm clouds gathering over the historic church in Dingli, creating a powerful contrast',
            location: 'Dingli, Malta',
            keywords: 'storm photography, Dingli church, dramatic weather, church architecture, Malta storms'
        },
        'September 2019 mellieha 3 copy': {
            title: 'Mellieha Storm September 2019',
            description: 'Powerful storm system over Mellieha during September 2019, showcasing nature\'s dramatic force',
            location: 'Mellieha, Malta',
            keywords: 'Mellieha storm, September 2019, dramatic weather, storm photography, Malta weather'
        },
        'Road to nowhere storm mellieha sept 2019 copy': {
            title: 'Storm on the Road to Nowhere',
            description: 'A desolate road in Mellieha during a September 2019 storm, creating an atmospheric and moody scene',
            location: 'Mellieha, Malta',
            keywords: 'desolate road, Mellieha storm, atmospheric photography, moody weather, September 2019'
        },
        'Riviera-10.12.2022': {
            title: 'December Storm at Riviera',
            description: 'Winter storm over the Riviera coastline in December 2022, with dramatic waves and storm clouds',
            location: 'Riviera, Malta',
            keywords: 'December storm, Riviera Malta, winter weather, dramatic waves, 2022 storms'
        },
        'October-2021-Church-Dingly-copy': {
            title: 'October Storm Over Dingli Church',
            description: 'Autumn storm clouds gathering over the historic church in Dingli during October 2021',
            location: 'Dingli, Malta',
            keywords: 'October storm, Dingli church, autumn weather, dramatic clouds, 2021 storms'
        },
        'Mellieha 2nd Storm Sept 2019 5 copy': {
            title: 'Second Storm of September 2019',
            description: 'The second major storm to hit Mellieha in September 2019, captured in dramatic black and white',
            location: 'Mellieha, Malta',
            keywords: 'second storm, Mellieha Malta, September 2019, dramatic weather, storm sequence'
        },
        'Il Munqar 4 copy': {
            title: 'Storm Over Il Munqar',
            description: 'Dramatic storm clouds gathering over the Il Munqar area, creating an intense atmospheric scene',
            location: 'Il Munqar, Malta',
            keywords: 'Il Munqar storm, dramatic weather, atmospheric photography, Malta storms, cloud formations'
        },
        'Il Munqar 6 copy': {
            title: 'Lightning at Il Munqar',
            description: 'Electric lightning illuminating the night sky over Il Munqar during a powerful storm',
            location: 'Il Munqar, Malta',
            keywords: 'lightning photography, Il Munqar Malta, dramatic weather, night storm, electric atmosphere'
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

// Helper function to extract folder name from full path
function extractFolderName(fullPath) {
    // Extract the folder name from the full Windows path
    const pathParts = fullPath.split('\\');
    const imagesIndex = pathParts.findIndex(part => part === 'images');
    if (imagesIndex !== -1 && imagesIndex + 1 < pathParts.length) {
        return pathParts[imagesIndex + 1];
    }
    return null;
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
    const galleryImages = imageMapping.filter(img => {
        const folderName = extractFolderName(img.folder);
        
        // Check if folder matches
        if (folderName !== gallery.folder) {
            return false;
        }
        
        // Apply special filters
        if (gallery.filter) {
            return img.original.includes(gallery.filter);
        }
        
        // Apply exclusions
        if (gallery.exclude) {
            return !gallery.exclude.some(excludeTerm => 
                img.original.includes(excludeTerm)
            );
        }
        
        return true;
    });
    
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
        
        // Add loading and error handling
        const img = imageElement.querySelector('img');
        if (img) {
            img.addEventListener('load', () => {
                imageElement.classList.remove('loading');
            });
            
            img.addEventListener('error', () => {
                imageElement.classList.remove('loading');
                imageElement.classList.add('error');
                console.warn(`Failed to load image: ${image.original}`);
            });
            
            // Add loading class initially
            imageElement.classList.add('loading');
        }
        
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

// Commission inquiry function
function openCommissionInquiry(series) {
    const subject = encodeURIComponent(`Commission Inquiry: ${series}`);
    const body = encodeURIComponent(`Hello Adel,\n\nI'm interested in commissioning photography work for the ${series} series.\n\nPlease provide information about:\n- Commission process\n- Timeline\n- Pricing\n- Requirements\n\nThank you,\n[Your Name]`);
    window.open(`mailto:ferritography@gmail.com?subject=${subject}&body=${body}`);
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