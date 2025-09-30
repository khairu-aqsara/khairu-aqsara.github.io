# Khairu Aqsara - Personal Blog

A modern, high-performance personal blog built with Hugo and the PaperMod theme. Features comprehensive SEO optimization, full-text search, responsive design, and Progressive Web App capabilities.

## 🚀 Quick Start

### Prerequisites

- **Hugo Extended** >= 0.115 ([Download](https://gohugo.io/installation/))
- **Git** for version control
- **Node.js** (optional, for advanced development)

### Installation

```bash
# Clone the repository
git clone --recurse-submodules https://github.com/khairu-aqsara/khairu-aqsara.github.io.git
cd khairu-aqsara.github.io

# Update theme submodule
git submodule update --init --recursive

# Install Hugo (if not already installed)
# On macOS with Homebrew:
brew install hugo

# On Windows with Chocolatey:
# choco install hugo-extended

# On Linux:
# sudo snap install hugo --channel=extended
```

### Development

```bash
# Start development server
hugo server --buildDrafts

# Build for production
hugo --minify

# Run validation tests
python3 run_all_tests.py

# SEO & Performance testing
python3 seo_performance_test.py
```

## 📊 Features

### 🔍 **Search & Discovery**
- **Full-text search** with Fuse.js (client-side, no server required)
- **Keyboard shortcuts** (`Ctrl+K` or `/` for quick search access)
- **Advanced search index** with 5+ searchable content types
- **SEO optimization** with structured data and meta tags

### 📱 **Modern Web Standards**
- **Progressive Web App** (PWA) with offline support
- **Responsive design** optimized for all device sizes
- **Dark/Light theme** with system preference detection
- **Service Worker** for intelligent caching and performance

### ⚡ **Performance Optimized**
- **11KB homepage** with aggressive optimization
- **Asset fingerprinting** for cache optimization
- **Lazy loading** for images and resources
- **Critical CSS inlining** for above-the-fold content
- **83.3% SEO score** with comprehensive optimization

### 📝 **Content Management**
- **Markdown-based** content with Hugo's powerful processing
- **Custom archetypes** for consistent post formatting
- **Responsive images** with WebP support and multiple formats
- **Tag and category** organization with automatic taxonomy pages

## 🏗️ Architecture

### **Site Structure**
```
├── archetypes/          # Content templates
├── assets/             # Source assets (SCSS, JS)
├── content/            # Markdown content
│   ├── posts/         # Blog posts
│   ├── pages/         # Static pages
│   └── search.md      # Search page
├── layouts/           # Custom templates
│   ├── partials/      # Reusable components
│   └── shortcodes/    # Custom shortcodes
├── static/            # Static assets
│   ├── images/        # Image files
│   ├── sw.js          # Service Worker
│   └── manifest.json  # PWA manifest
├── themes/PaperMod/   # Hugo theme (submodule)
└── public/            # Generated site (excluded from repo)
```

### **Technology Stack**
- **Hugo** v0.150+ (Static Site Generator)
- **PaperMod** (Hugo theme with customizations)  
- **Fuse.js** (Client-side search)
- **Service Worker** (PWA and caching)
- **Hugo Pipes** (Asset processing)
- **GitHub Actions** (CI/CD deployment)

## 📚 Documentation

### **Content Creation**
- [Content Authoring Guide](docs/content-guide.md) - How to write and publish posts
- [Theme Customization](docs/theme-customization.md) - Customizing design and layout

### **Development**
- [Testing Guide](#testing) - Running validation and performance tests
- [Deployment Guide](#deployment) - Production deployment process
- [Performance Guide](#performance) - Optimization best practices

## 🧪 Testing

### **Automated Testing Suite**

```bash
# Run comprehensive validation
python3 run_all_tests.py

# Individual test components
python3 validate_content.py    # Content quality validation
python3 test_site.py          # Site functionality testing  
python3 check_links.py        # Link integrity validation
python3 seo_performance_test.py # SEO & performance analysis
```

### **Testing Coverage**
- ✅ **Content Validation**: Frontmatter, markdown syntax, structure
- ✅ **Site Functionality**: Search, navigation, essential pages
- ✅ **Performance**: File sizes, optimization, Core Web Vitals prep
- ✅ **SEO**: Meta tags, structured data, social sharing
- ✅ **Accessibility**: ARIA labels, semantic HTML, keyboard nav
- ✅ **Links**: Internal link validation, asset verification

### **Performance Benchmarks**
```
📊 Current Performance Metrics:
├── SEO Score: 83.3% (Excellent)
├── Homepage: 11.0KB (Optimal) 
├── Build Time: ~130ms (Fast)
├── Search Index: 21.8KB (Efficient)
└── Total Assets: <50KB initial load
```

## 🚀 Deployment

### **GitHub Pages (Automatic)**

The site automatically deploys to GitHub Pages via GitHub Actions when changes are pushed to the main branch.

```bash
# Deploy to production
git add .
git commit -m "Update content"
git push origin main
```

### **Manual Deployment**

```bash
# Build for production
hugo --minify

# Verify build
python3 seo_performance_test.py

# Deploy to your preferred hosting platform
# (Upload contents of public/ directory)
```

### **Environment Configuration**

Create `.env` file for local development:
```bash
HUGO_ENV=development
HUGO_BASEURL=http://localhost:1313
```

## 🛠️ Customization

### **Site Configuration**

Edit `hugo.toml` to customize:
- Site title, description, and metadata
- Social media links and profiles
- Menu structure and navigation
- SEO and performance settings
- Search configuration

### **Theme Customization**

See [Theme Customization Guide](docs/theme-customization.md) for:
- Custom CSS and styling
- Layout modifications
- Component customization
- Adding new features

### **Content Types**

Use Hugo's archetype system:
```bash
# Create new blog post
hugo new posts/my-new-post.md

# Create new page
hugo new pages/my-new-page.md
```

## 📈 Analytics & Monitoring

### **Performance Monitoring**
- **Core Web Vitals**: Monitor LCP, FID, CLS metrics
- **Lighthouse CI**: Automated performance testing
- **Build Performance**: Track Hugo build times and asset sizes

### **SEO Monitoring**
- **Google Search Console**: Monitor search performance
- **Social Media**: Track Open Graph and Twitter Card previews
- **Structured Data**: Validate rich snippets and schema markup

## 🔧 Troubleshooting

### **Common Issues**

**Build Errors**
```bash
# Clear Hugo cache
hugo --cleanDestinationDir

# Rebuild with verbose output
hugo --minify --verbose
```

**Search Not Working**
```bash
# Verify search index generation
ls -la public/index.json

# Test search functionality
grep -q "searchInput" public/search/index.html
```

**Performance Issues**
```bash
# Run performance analysis
python3 seo_performance_test.py

# Check asset sizes
du -sh public/assets/*
```

### **Development Tips**

- Use `hugo server --buildDrafts` for development
- Run tests before committing changes
- Optimize images before adding to `/static/images/`
- Validate content with automated testing suite

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### **Development Workflow**
```bash
# Setup development environment
git clone --recurse-submodules [your-fork]
cd khairu-aqsara.github.io
hugo server --buildDrafts

# Make changes and test
python3 run_all_tests.py

# Commit and push
git add .
git commit -m "Your changes"
git push origin your-branch
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugo** - The world's fastest framework for building websites
- **PaperMod** - Beautiful and fast Hugo theme
- **Fuse.js** - Lightweight fuzzy-search library
- **GitHub Pages** - Free hosting for static sites

## 📞 Support

- **Documentation**: [docs/](docs/) directory
- **Issues**: [GitHub Issues](https://github.com/khairu-aqsara/khairu-aqsara.github.io/issues)  
- **Discussions**: [GitHub Discussions](https://github.com/khairu-aqsara/khairu-aqsara.github.io/discussions)
- **Email**: [wenkhairu@gmail.com](mailto:wenkhairu@gmail.com)

---

**Built with ❤️ using Hugo and deployed on GitHub Pages**

*Last updated: 2025-09-30*
