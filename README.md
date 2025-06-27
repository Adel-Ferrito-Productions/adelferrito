# Adel Ferrito Photography Website

A modern, responsive photography portfolio website showcasing fine art photography from Malta and Sicily.

## 🏗️ Project Structure

```
adelferrito/
├── Index.html                 # Main HTML file (now modular)
├── CSS/
│   └── main.css              # All styles extracted from HTML
├── JS/
│   ├── main.js               # Main application logic
│   ├── gallery.js            # Gallery functionality
│   └── animations.js         # Scroll animations and interactions
├── Assets/
│   ├── images/               # Organized image directories
│   │   ├── featured/         # Hero/featured images
│   │   ├── storms/           # Storm photography
│   │   ├── bw-malta/         # Black & white Malta
│   │   ├── bw-sicily/        # Black & white Sicily
│   │   ├── golden-hour/      # Sunrise/sunset photography
│   │   ├── dramatic-architecture/ # Architectural studies
│   │   ├── landscapes/       # Mediterranean landscapes
│   │   ├── salinunte/        # Ancient Greek ruins
│   │   ├── caltabellotta/    # Medieval Sicilian village
│   │   └── grotte/           # Cave photography
│   ├── Logo/                 # Logo assets
│   └── Website pics/         # Original image organization
└── README.md                 # This file
```

## ✨ Features

### ✅ Implemented
- **Responsive Design**: Mobile-first approach with breakpoints
- **Safari Compatibility**: Fixed backdrop-filter issue
- **Modular Architecture**: Separated CSS and JavaScript
- **SEO Optimized**: Meta tags, Open Graph, semantic HTML
- **Performance**: Lazy loading, image preloading, optimized fonts
- **Accessibility**: Keyboard navigation, screen reader friendly
- **Gallery System**: Modal galleries with lightbox functionality
- **Smooth Animations**: Fade-in effects, scroll animations
- **Error Handling**: Graceful fallbacks for missing images

### 🚧 In Progress
- Image optimization and WebP support
- Progressive image loading
- Advanced performance monitoring

## 🛠️ Development

### Prerequisites
- Modern web browser
- Local development server (optional)

### Setup
1. Clone or download the project
2. Open `Index.html` in a web browser
3. For development, use a local server:
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   ```

### File Organization

#### CSS (`CSS/main.css`)
- **Global Styles**: Reset, variables, typography
- **Navigation**: Navbar, menu, responsive behavior
- **Layout**: Grid systems, sections, containers
- **Components**: Buttons, cards, modals, lightbox
- **Responsive**: Mobile breakpoints and adaptations
- **Animations**: Transitions, hover effects, fade-ins

#### JavaScript Modules

**`JS/main.js`** - Application Core
- DOM ready initialization
- Error handling for images
- Performance monitoring
- Utility functions

**`JS/gallery.js`** - Gallery System
- Gallery configurations
- Modal management
- Lightbox functionality
- SEO title/description updates

**`JS/animations.js`** - Interactions
- Scroll effects
- Smooth scrolling
- Intersection Observer animations
- Keyboard shortcuts

## 📱 Browser Support

- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+ (with backdrop-filter fix)
- **Edge**: 90+
- **Mobile**: iOS Safari 14+, Chrome Mobile 90+

## 🎨 Design System

### Colors
```css
--primary-black: #1a1a1a
--soft-black: #2a2a2a
--warm-white: #fefefe
--cool-gray: #8a8a8a
--light-gray: #f5f5f5
--accent-gray: #e8e8e8
```

### Typography
- **Headings**: Crimson Text (serif)
- **Body**: Inter (sans-serif)
- **Weights**: 300 (light), 400 (regular), 600 (semibold)

### Breakpoints
- **Mobile**: < 768px
- **Desktop**: ≥ 768px

## 📸 Image Requirements

### Featured Images
- **Format**: JPG, WebP (recommended)
- **Dimensions**: 1200x800px minimum
- **File Names**: `storm-hero.jpg`, `malta-bw-hero.jpg`, `sicily-bw-hero.jpg`
- **Location**: `Assets/images/featured/`

### Gallery Images
- **Format**: JPG, WebP (recommended)
- **Dimensions**: 800x600px minimum
- **Naming**: Descriptive with location and date
- **Location**: Respective category folders in `Assets/images/`

## 🔧 Customization

### Adding New Galleries
1. Add gallery configuration to `JS/gallery.js`
2. Create corresponding image folder
3. Add images with proper naming convention
4. Update navigation if needed

### Modifying Styles
1. Edit `CSS/main.css`
2. Use CSS custom properties for consistent theming
3. Test responsive behavior across devices

### Performance Optimization
1. Optimize images (compress, resize)
2. Convert to WebP format
3. Implement lazy loading for non-critical images
4. Monitor Core Web Vitals

## 🚀 Deployment

### Production Checklist
- [ ] Optimize all images
- [ ] Minify CSS and JavaScript
- [ ] Enable gzip compression
- [ ] Set up CDN for assets
- [ ] Configure caching headers
- [ ] Test across all target browsers
- [ ] Validate HTML and accessibility

### Hosting Recommendations
- **Static Hosting**: Netlify, Vercel, GitHub Pages
- **CDN**: Cloudflare, AWS CloudFront
- **Image Optimization**: Cloudinary, ImageKit

## 📊 Performance Metrics

### Target Scores
- **Lighthouse Performance**: 90+
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

## 🐛 Known Issues

### Fixed
- ✅ Safari backdrop-filter compatibility
- ✅ Monolithic file structure
- ✅ Missing asset directories

### To Address
- 🔄 Image optimization pipeline
- 🔄 WebP format implementation
- 🔄 Advanced error handling
- 🔄 Loading state improvements

## 📝 Changelog

### v2.0.0 (Current)
- **BREAKING**: Modularized codebase
- **FEATURE**: Safari compatibility fix
- **IMPROVEMENT**: Separated CSS and JavaScript
- **FEATURE**: Error handling for missing images
- **IMPROVEMENT**: Performance monitoring

### v1.0.0 (Original)
- Initial monolithic implementation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test across browsers
5. Submit a pull request

## 📄 License

© 2025 Adel Ferrito. All rights reserved.

## 📞 Support

For technical support or questions:
- **Email**: ferritography@gmail.com
- **Location**: Malta & Sicily

---

**Built with ❤️ for showcasing fine art photography** 