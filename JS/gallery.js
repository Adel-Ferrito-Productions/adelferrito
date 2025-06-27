// Gallery configurations with SEO-optimized content
const galleries = {
    'storms': {
        title: 'Storm Studies',
        description: 'Mediterranean thunderstorms captured with dramatic intensity, showcasing the raw power and sublime beauty of nature\'s most spectacular displays.',
        seoTitle: 'Storm Photography Malta Sicily - Lightning and Dramatic Weather',
        folder: 'storms',
        images: [
            { file: 'malta-lightning-strike-01.jpg', title: 'Lightning Strike Malta', details: 'Valletta Harbor, 2024' },
            { file: 'sicily-thunderstorm-02.jpg', title: 'Sicilian Thunderstorm', details: 'Mount Etna Region, 2024' },
            { file: 'mediterranean-storm-clouds-03.jpg', title: 'Storm Clouds', details: 'Gozo Channel, 2024' },
            { file: 'dramatic-lightning-bolts-04.jpg', title: 'Electric Storm', details: 'Malta Coastline, 2024' },
            { file: 'storm-over-valletta-05.jpg', title: 'Storm Over Valletta', details: 'Grand Harbor, 2024' },
            { file: 'lightning-mediterranean-06.jpg', title: 'Mediterranean Lightning', details: 'Open Waters, 2024' }
        ]
    },
    'malta-bw': {
        title: 'Malta: Black & White',
        description: 'Timeless monochrome studies of Malta\'s dramatic landscapes, ancient architecture, and Mediterranean character rendered in fine art black and white.',
        seoTitle: 'Malta Black and White Photography - Fine Art Monochrome Landscapes',
        folder: 'bw-malta',
        images: [
            { file: 'valletta-architecture-bw-01.jpg', title: 'Valletta Architecture', details: 'Upper Barrakka Gardens, 2024' },
            { file: 'malta-coastline-dramatic-02.jpg', title: 'Dramatic Coastline', details: 'Dingli Cliffs, 2024' },
            { file: 'mdina-medieval-streets-03.jpg', title: 'Mdina Streets', details: 'Silent City, 2024' },
            { file: 'golden-bay-monochrome-04.jpg', title: 'Golden Bay', details: 'Northwestern Coast, 2024' },
            { file: 'grand-harbor-bw-05.jpg', title: 'Grand Harbor', details: 'From Upper Barrakka, 2024' },
            { file: 'blue-grotto-shadows-06.jpg', title: 'Blue Grotto', details: 'Southern Malta, 2024' }
        ]
    },
    'sicily-bw': {
        title: 'Sicily: Echoes of Time',
        description: 'A meditation on Sicily\'s layered history through black and white photography, from ancient Greek ruins to medieval hilltop villages.',
        seoTitle: 'Sicily Black and White Photography - Ancient Ruins and Medieval Towns',
        folder: 'bw-sicily',
        images: [
            { file: 'selinunte-ruins-dramatic-01.jpg', title: 'Selinunte Temple', details: 'Ancient Greek Ruins, 2024' },
            { file: 'caltabellotta-hilltop-02.jpg', title: 'Caltabellotta Village', details: 'Medieval Hilltop, 2024' },
            { file: 'etna-landscape-bw-03.jpg', title: 'Mount Etna', details: 'Volcanic Landscape, 2024' },
            { file: 'taormina-ancient-theater-04.jpg', title: 'Taormina Theater', details: 'Greek-Roman Ruins, 2024' },
            { file: 'agrigento-valley-temples-05.jpg', title: 'Valley of Temples', details: 'Agrigento, 2024' },
            { file: 'sicilian-countryside-06.jpg', title: 'Sicilian Countryside', details: 'Central Sicily, 2024' }
        ]
    },
    'golden-hour': {
        title: 'Golden Hour',
        description: 'The transformative quality of Mediterranean light during sunrise and sunset, capturing the poetry of changing illumination.',
        seoTitle: 'Golden Hour Photography Malta Sicily - Sunrise and Sunset Fine Art',
        folder: 'golden-hour',
        images: [
            { file: 'malta-sunrise-golden-01.jpg', title: 'Malta Sunrise', details: 'St. Peter\'s Pool, 2024' },
            { file: 'sicily-sunset-dramatic-02.jpg', title: 'Sicilian Sunset', details: 'Western Coast, 2024' },
            { file: 'valletta-golden-light-03.jpg', title: 'Valletta Golden Hour', details: 'Fortifications, 2024' },
            { file: 'gozo-sunrise-cliffs-04.jpg', title: 'Gozo Sunrise', details: 'Ta\' Cenc Cliffs, 2024' },
            { file: 'mediterranean-sunset-05.jpg', title: 'Mediterranean Sunset', details: 'Open Waters, 2024' },
            { file: 'fisherman-golden-hour-06.jpg', title: 'Fisherman at Dawn', details: 'Marsaxlokk, 2024' }
        ]
    },
    'architecture': {
        title: 'Architectural Studies',
        description: 'The dialogue between light, form, and space in Mediterranean architecture, from ancient temples to contemporary design.',
        seoTitle: 'Architectural Photography Malta Sicily - Ancient and Modern Buildings',
        folder: 'dramatic-architecture',
        images: [
            { file: 'st-johns-cathedral-01.jpg', title: 'St. John\'s Cathedral', details: 'Valletta Interior, 2024' },
            { file: 'modern-architecture-malta-02.jpg', title: 'Contemporary Malta', details: 'Sliema Waterfront, 2024' },
            { file: 'palazzo-parisio-03.jpg', title: 'Palazzo Parisio', details: 'Naxxar, 2024' },
            { file: 'fortification-walls-04.jpg', title: 'Fortification Walls', details: 'Valletta Bastions, 2024' },
            { file: 'traditional-balconies-05.jpg', title: 'Traditional Balconies', details: 'Valletta Streets, 2024' },
            { file: 'church-dome-silhouette-06.jpg', title: 'Church Dome', details: 'Mosta Rotunda, 2024' }
        ]
    },
    'landscapes': {
        title: 'Mediterranean Landscapes',
        description: 'The diverse terrains and coastal beauty of Malta and Sicily captured through an artistic lens, revealing hidden poetry in familiar places.',
        seoTitle: 'Mediterranean Landscape Photography - Malta and Sicily Fine Art',
        folder: 'landscapes',
        images: [
            { file: 'mediterranean-coastline-01.jpg', title: 'Mediterranean Coast', details: 'Rocky Shoreline, 2024' },
            { file: 'malta-countryside-02.jpg', title: 'Maltese Countryside', details: 'Agricultural Terraces, 2024' },
            { file: 'sicily-rolling-hills-03.jpg', title: 'Sicilian Hills', details: 'Central Landscape, 2024' },
            { file: 'crystal-lagoon-04.jpg', title: 'Crystal Lagoon', details: 'Comino Blue Lagoon, 2024' },
            { file: 'volcanic-landscape-05.jpg', title: 'Volcanic Terrain', details: 'Mount Etna Slopes, 2024' },
            { file: 'fishing-village-06.jpg', title: 'Fishing Village', details: 'Marsaxlokk Harbor, 2024' }
        ]
    },
    'salinunte': {
        title: 'Selinunte',
        description: 'Ancient Greek ruins where history and landscape converge in timeless composition, capturing the dialogue between past and present.',
        seoTitle: 'Selinunte Archaeological Photography - Ancient Greek Ruins Sicily',
        folder: 'salinunte',
        images: [
            { file: 'temple-e-selinunte-01.jpg', title: 'Temple E', details: 'Eastern Hill, 2024' },
            { file: 'temple-columns-detail-02.jpg', title: 'Column Details', details: 'Doric Architecture, 2024' },
            { file: 'selinunte-overview-03.jpg', title: 'Archaeological Overview', details: 'Ancient City, 2024' },
            { file: 'temple-ruins-sunset-04.jpg', title: 'Ruins at Sunset', details: 'Golden Light, 2024' },
            { file: 'fallen-capitals-05.jpg', title: 'Fallen Capitals', details: 'Weathered Stone, 2024' },
            { file: 'selinunte-landscape-06.jpg', title: 'Sacred Landscape', details: 'Temple Complex, 2024' }
        ]
    },
    'caltabellotta': {
        title: 'Caltabellotta',
        description: 'A medieval Sicilian village perched between earth and sky, captured in monochrome poetry that speaks of centuries and silence.',
        seoTitle: 'Caltabellotta Photography - Medieval Sicilian Village Black and White',
        folder: 'caltabellotta',
        images: [
            { file: 'caltabellotta-village-01.jpg', title: 'Village Overview', details: 'Hilltop Settlement, 2024' },
            { file: 'medieval-streets-02.jpg', title: 'Medieval Streets', details: 'Stone Pathways, 2024' },
            { file: 'castle-ruins-03.jpg', title: 'Castle Ruins', details: 'Norman Fortress, 2024' },
            { file: 'church-bell-tower-04.jpg', title: 'Bell Tower', details: 'Chiesa Madre, 2024' },
            { file: 'valley-view-05.jpg', title: 'Valley Vista', details: 'Panoramic View, 2024' },
            { file: 'ancient-walls-06.jpg', title: 'Ancient Walls', details: 'Medieval Fortifications, 2024' }
        ]
    },
    'caves': {
        title: 'Hidden Grottos',
        description: 'The secret chambers and coastal caves where light becomes sculpture, revealing nature\'s hidden architecture beneath the surface.',
        seoTitle: 'Cave Photography Malta Sicily - Hidden Grottos and Coastal Caves',
        folder: 'grotte',
        images: [
            { file: 'blue-grotto-interior-01.jpg', title: 'Blue Grotto Interior', details: 'Natural Cave, 2024' },
            { file: 'coastal-cave-light-02.jpg', title: 'Cave Light Shaft', details: 'Limestone Formation, 2024' },
            { file: 'underwater-cave-03.jpg', title: 'Underwater Cave', details: 'Submerged Chamber, 2024' },
            { file: 'stalactite-formations-04.jpg', title: 'Stalactite Forms', details: 'Cave Ceiling, 2024' },
            { file: 'grotto-reflection-05.jpg', title: 'Grotto Reflection', details: 'Water Surface, 2024' },
            { file: 'cave-entrance-dramatic-06.jpg', title: 'Cave Entrance', details: 'Natural Arch, 2024' }
        ]
    }
};

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
    
    gallery.images.forEach((image, index) => {
        const imageElement = document.createElement('div');
        imageElement.className = 'gallery-image';
        imageElement.onclick = () => openLightbox(`assets/images/${gallery.folder}/${image.file}`, `${image.title} - ${image.details} - Fine art photography by Adel Ferrito`);
        
        imageElement.innerHTML = `
            <img src="assets/images/${gallery.folder}/${image.file}" 
                 alt="${image.title} - ${image.details} - ${gallery.seoTitle} by Adel Ferrito"
                 loading="lazy">
            <div class="image-info">
                <div class="image-title">${image.title}</div>
                <div class="image-details">${image.details}</div>
            </div>
        `;
        
        galleryGrid.appendChild(imageElement);
    });
    
    document.getElementById('galleryModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
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

function openLightbox(imageSrc, imageAlt) {
    const lightbox = document.getElementById('lightbox');
    const lightboxImage = document.getElementById('lightboxImage');
    
    lightboxImage.src = imageSrc;
    lightboxImage.alt = imageAlt;
    lightbox.style.display = 'block';
}

function closeLightbox() {
    document.getElementById('lightbox').style.display = 'none';
}

// Export functions for use in main.js
window.openGallery = openGallery;
window.closeGallery = closeGallery;
window.openLightbox = openLightbox;
window.closeLightbox = closeLightbox; 