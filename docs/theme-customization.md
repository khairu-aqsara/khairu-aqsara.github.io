# Theme Customization Guide

Complete guide for customizing the PaperMod theme and extending the Hugo blog functionality.

## 🎨 Theme Architecture

### **PaperMod Structure**
```
themes/PaperMod/
├── assets/               # Source assets (SCSS, JS)
├── layouts/             # Template files
│   ├── _default/       # Base templates
│   ├── partials/       # Reusable components
│   └── shortcodes/     # Content shortcodes
├── static/             # Static theme assets
└── hugo.toml           # Theme configuration
```

### **Custom Overrides**
```
layouts/                 # Local overrides (takes precedence)
├── _default/           # Override base templates
├── partials/           # Custom components
│   ├── seo.html       # Enhanced SEO
│   ├── performance.html # Performance optimizations
│   └── extend_head.html # Head extensions
└── shortcodes/         # Custom shortcodes
    └── responsive-image.html
```

## 🔧 Configuration Customization

### **Site Configuration** (`hugo.toml`)

#### **Basic Settings**
```toml
baseURL = "https://your-domain.com"
languageCode = "en-us"
title = "Your Blog Title"
theme = "PaperMod"
defaultContentLanguage = "en"
enableRobotsTXT = true
enableGitInfo = true
enableEmoji = true
```

#### **Build Configuration**
```toml
[build]
  writeStats = true

[minify]
  disableXML = false
  minifyOutput = true
```

#### **Markup Configuration**
```toml
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true  # Allow HTML in markdown
      hardWraps = false
    [markup.goldmark.parser]
      autoHeadingID = true
      autoHeadingIDType = "github"
  [markup.highlight]
    style = "github"
    lineNos = true
    lineNumbersInTable = false
    tabWidth = 4
```

### **Theme Parameters**

#### **Site Identity**
```toml
[params]
  author = "Your Name"
  description = "Your blog description"
  keywords = ["keyword1", "keyword2", "keyword3"]
  defaultImage = "/images/default-social-image.jpg"
```

#### **Display Options**
```toml
[params]
  defaultTheme = "auto"  # auto, light, dark
  disableThemeToggle = false
  ShowReadingTime = true
  ShowShareButtons = true
  ShowPostNavLinks = true
  ShowBreadCrumbs = true
  ShowCodeCopyButtons = true
  ShowWordCount = true
  UseHugoToc = true
```

#### **Homepage Configuration**
```toml
[params.homeInfoParams]
  Title = "Welcome Message"
  Content = "Homepage description content"

[[params.socialIcons]]
  name = "github"
  url = "https://github.com/yourusername"

[[params.socialIcons]]
  name = "linkedin"
  url = "https://linkedin.com/in/yourprofile"

[[params.socialIcons]]
  name = "email"
  url = "mailto:your@email.com"
```

#### **Search Configuration**
```toml
[params.fuseOpts]
  isCaseSensitive = false
  shouldSort = true
  location = 0
  distance = 1000
  threshold = 0.4
  minMatchCharLength = 2
  limit = 10
  keys = ["title", "permalink", "summary", "content"]
```

## 🎨 CSS Customization

### **Custom Stylesheets**

Create `assets/css/custom.scss`:
```scss
// Custom variables
:root {
  --custom-primary: #007acc;
  --custom-secondary: #6c757d;
  --custom-accent: #28a745;
  
  // Override theme variables
  --theme: var(--custom-primary);
  --primary: var(--custom-secondary);
}

// Custom styles
.custom-header {
  background: linear-gradient(135deg, var(--custom-primary), var(--custom-accent));
  color: white;
  padding: 2rem;
  border-radius: 8px;
}

.highlight-box {
  background: var(--code-bg);
  border-left: 4px solid var(--custom-primary);
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 0 4px 4px 0;
}

// Responsive customizations
@media (max-width: 768px) {
  .custom-header {
    padding: 1rem;
    border-radius: 4px;
  }
}
```

### **Dark Mode Customization**
```scss
// Dark mode specific styles
[data-theme="dark"] {
  --custom-bg: #1a1a1a;
  --custom-text: #e0e0e0;
  --custom-border: #333;
}

.dark {
  .custom-header {
    background: linear-gradient(135deg, #0056b3, #1e7e34);
  }
  
  .highlight-box {
    background: var(--custom-bg);
    border-color: var(--custom-accent);
  }
}
```

### **Typography Customization**
```scss
// Font imports
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

// Custom typography
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  line-height: 1.3;
}

.post-content {
  font-size: 1.1rem;
  
  h2 {
    margin-top: 2rem;
    margin-bottom: 1rem;
    color: var(--custom-primary);
  }
  
  p {
    margin-bottom: 1.5rem;
  }
  
  code {
    background: var(--code-bg);
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-size: 0.9em;
  }
}
```

## 🧩 Layout Customization

### **Custom Templates**

#### **Enhanced Single Post Layout**
Create `layouts/_default/single.html`:
```html
{{- define "main" }}

<article class="post-single">
  <!-- Custom header -->
  <header class="entry-header custom-header">
    <h1 class="entry-title">{{ .Title }}</h1>
    {{- if .Description }}
    <div class="entry-description">{{ .Description }}</div>
    {{- end }}
    
    <!-- Post metadata -->
    <div class="post-meta">
      <time datetime="{{ .Date.Format "2006-01-02T15:04:05Z07:00" }}">
        {{ .Date.Format "January 2, 2006" }}
      </time>
      {{- with .Params.author }} • By {{ . }}{{- end }}
      {{- if .ReadingTime }} • {{ .ReadingTime }} min read{{- end }}
    </div>
  </header>

  <!-- Table of contents -->
  {{- if (.Param "ShowToc") }}
  {{- partial "toc.html" . }}
  {{- end }}

  <!-- Post content -->
  <div class="entry-content">
    {{- .Content }}
  </div>

  <!-- Post footer -->
  <footer class="entry-footer">
    {{- partial "post_tags.html" . }}
    {{- partial "share_buttons.html" . }}
  </footer>

  <!-- Navigation -->
  {{- if (.Param "ShowPostNavLinks") }}
  {{- partial "post_nav_links.html" . }}
  {{- end }}
</article>

{{- end }}{{/* end main */}}
```

#### **Custom Homepage Layout**
Create `layouts/index.html`:
```html
{{- define "main" }}

<!-- Hero section -->
<section class="hero-section">
  <div class="hero-content">
    <h1>{{ site.Params.homeInfoParams.Title }}</h1>
    <p>{{ site.Params.homeInfoParams.Content }}</p>
    
    <!-- Call-to-action buttons -->
    <div class="hero-actions">
      <a href="/posts/" class="btn btn-primary">Read Posts</a>
      <a href="/search/" class="btn btn-secondary">Search Content</a>
    </div>
  </div>
</section>

<!-- Recent posts -->
<section class="recent-posts">
  <h2>Recent Posts</h2>
  <div class="post-grid">
    {{- range first 6 (where site.RegularPages "Type" "posts") }}
    <article class="post-card">
      {{- if .Params.cover.image }}
      <div class="post-image">
        <img src="{{ .Params.cover.image }}" alt="{{ .Params.cover.alt | default .Title }}">
      </div>
      {{- end }}
      
      <div class="post-content">
        <h3><a href="{{ .RelPermalink }}">{{ .Title }}</a></h3>
        <p>{{ .Summary }}</p>
        
        <div class="post-meta">
          <time>{{ .Date.Format "Jan 2, 2006" }}</time>
          {{- if .ReadingTime }} • {{ .ReadingTime }} min{{- end }}
        </div>
      </div>
    </article>
    {{- end }}
  </div>
</section>

{{- end }}{{/* end main */}}
```

### **Custom Partials**

#### **Enhanced Navigation**
Create `layouts/partials/header.html`:
```html
<header class="header">
  <nav class="nav">
    <div class="logo">
      <a href="{{ "/" | absURL }}" accesskey="h" title="Home">
        {{- if site.Params.logo }}
        <img src="{{ site.Params.logo }}" alt="{{ site.Title }}">
        {{- else }}
        {{ site.Title }}
        {{- end }}
      </a>
    </div>

    <!-- Mobile menu toggle -->
    <button class="menu-toggle" aria-label="Toggle menu">
      <span></span>
      <span></span>
      <span></span>
    </button>

    <!-- Navigation menu -->
    <ul class="menu" id="menu">
      {{- range site.Menus.main }}
      <li>
        <a href="{{ .URL | absURL }}" title="{{ .Title | default .Name }}">
          {{- .Pre }}
          <span>{{ .Name }}</span>
          {{- .Post }}
        </a>
      </li>
      {{- end }}
      
      <!-- Theme toggle -->
      <li>
        <button id="theme-toggle" title="Toggle theme">
          <svg class="theme-icon sun"><!-- Sun icon --></svg>
          <svg class="theme-icon moon"><!-- Moon icon --></svg>
        </button>
      </li>
    </ul>
  </nav>
</header>
```

#### **Social Share Buttons**
Create `layouts/partials/share_buttons.html`:
```html
{{- if site.Params.ShowShareButtons }}
<div class="share-buttons">
  <h4>Share this post:</h4>
  
  <a href="https://twitter.com/intent/tweet?text={{ .Title }}&url={{ .Permalink }}" 
     target="_blank" rel="noopener" class="share-btn twitter">
    Twitter
  </a>
  
  <a href="https://www.linkedin.com/sharing/share-offsite/?url={{ .Permalink }}" 
     target="_blank" rel="noopener" class="share-btn linkedin">
    LinkedIn
  </a>
  
  <a href="https://www.facebook.com/sharer/sharer.php?u={{ .Permalink }}" 
     target="_blank" rel="noopener" class="share-btn facebook">
    Facebook
  </a>
  
  <button class="share-btn copy-link" data-url="{{ .Permalink }}">
    Copy Link
  </button>
</div>
{{- end }}
```

## 🔌 Custom Shortcodes

### **Enhanced Code Block**
Create `layouts/shortcodes/code.html`:
```html
{{- $lang := .Get 0 }}
{{- $title := .Get "title" }}
{{- $lineNos := .Get "lineNos" | default true }}

<div class="code-block-wrapper">
  {{- if $title }}
  <div class="code-title">{{ $title }}</div>
  {{- end }}
  
  <div class="code-block">
    <button class="copy-button" data-clipboard-target="#code-{{ .Ordinal }}">
      Copy
    </button>
    
    <pre id="code-{{ .Ordinal }}"><code class="language-{{ $lang }}">
      {{- .Inner | safeHTML }}
    </code></pre>
  </div>
</div>
```

### **Alert Box Shortcode**
Create `layouts/shortcodes/alert.html`:
```html
{{- $type := .Get 0 | default "info" }}
{{- $title := .Get "title" }}

<div class="alert alert-{{ $type }}">
  {{- if $title }}
  <div class="alert-title">{{ $title }}</div>
  {{- end }}
  
  <div class="alert-content">
    {{ .Inner | markdownify }}
  </div>
</div>
```

Usage in content:
```markdown
{{< alert "warning" "Important Note" >}}
This is a warning message with **markdown** support.
{{< /alert >}}

{{< code "javascript" title="Example Function" >}}
function example() {
    console.log("Hello, World!");
}
{{< /code >}}
```

### **Image Gallery Shortcode**
Create `layouts/shortcodes/gallery.html`:
```html
{{- $images := .Get "images" | split "," }}
{{- $class := .Get "class" | default "gallery" }}

<div class="image-gallery {{ $class }}">
  {{- range $images }}
  {{- $image := trim . " " }}
  <div class="gallery-item">
    <a href="{{ $image | absURL }}" data-lightbox="gallery">
      <img src="{{ $image | absURL }}" alt="Gallery image" loading="lazy">
    </a>
  </div>
  {{- end }}
</div>
```

## 📱 Mobile Optimization

### **Responsive Navigation**
```scss
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  
  .menu-toggle {
    display: none;
    flex-direction: column;
    background: none;
    border: none;
    cursor: pointer;
    
    span {
      width: 25px;
      height: 3px;
      background: var(--primary);
      margin: 3px 0;
      transition: 0.3s;
    }
  }
  
  @media (max-width: 768px) {
    .menu-toggle {
      display: flex;
    }
    
    .menu {
      position: fixed;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100vh;
      background: var(--theme);
      flex-direction: column;
      justify-content: center;
      transition: left 0.3s;
      
      &.active {
        left: 0;
      }
    }
  }
}
```

### **Mobile-First CSS**
```scss
// Mobile-first approach
.post-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
  
  // Tablet
  @media (min-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
  
  // Desktop
  @media (min-width: 1024px) {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
}

// Touch-friendly buttons
.btn {
  min-height: 44px;  // Apple's recommended touch target
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
```

## 🚀 Performance Customizations

### **Critical CSS Inlining**
Update `layouts/partials/extend_head.html`:
```html
{{- if .IsHome }}
<style>
/* Critical above-the-fold styles */
.header { /* styles */ }
.hero-section { /* styles */ }
.nav { /* styles */ }
</style>
{{- end }}

{{- if .IsPage }}
<style>
/* Critical post styles */
.post-single { /* styles */ }
.entry-header { /* styles */ }
</style>
{{- end }}
```

### **Resource Optimization**
```html
<!-- Preload critical resources -->
<link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{{ "css/critical.css" | absURL }}" as="style">

<!-- DNS prefetch for external resources -->
<link rel="dns-prefetch" href="//fonts.googleapis.com">
<link rel="dns-prefetch" href="//www.google-analytics.com">

<!-- Preconnect for critical third-party resources -->
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

## 🔧 JavaScript Customization

### **Enhanced Search**
Create `assets/js/enhanced-search.js`:
```javascript
class EnhancedSearch {
  constructor() {
    this.searchInput = document.getElementById('searchInput');
    this.searchResults = document.getElementById('searchResults');
    this.searchIndex = null;
    this.fuse = null;
    
    this.init();
  }
  
  async init() {
    await this.loadSearchIndex();
    this.setupEventListeners();
    this.setupKeyboardShortcuts();
  }
  
  async loadSearchIndex() {
    try {
      const response = await fetch('/index.json');
      this.searchIndex = await response.json();
      
      this.fuse = new Fuse(this.searchIndex, {
        keys: ['title', 'content', 'summary'],
        threshold: 0.4,
        includeScore: true
      });
    } catch (error) {
      console.error('Failed to load search index:', error);
    }
  }
  
  setupEventListeners() {
    this.searchInput?.addEventListener('input', 
      this.debounce(this.performSearch.bind(this), 300)
    );
  }
  
  setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Ctrl/Cmd + K for search
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        this.focusSearch();
      }
      
      // Escape to close search
      if (e.key === 'Escape') {
        this.clearSearch();
      }
    });
  }
  
  performSearch(query) {
    if (!this.fuse || !query.trim()) {
      this.clearResults();
      return;
    }
    
    const results = this.fuse.search(query, { limit: 10 });
    this.displayResults(results);
  }
  
  displayResults(results) {
    if (!results.length) {
      this.searchResults.innerHTML = '<li>No results found</li>';
      return;
    }
    
    const html = results.map(result => `
      <li class="search-result">
        <a href="${result.item.permalink}">
          <h3>${this.highlightMatches(result.item.title, query)}</h3>
          <p>${this.highlightMatches(result.item.summary, query)}</p>
        </a>
      </li>
    `).join('');
    
    this.searchResults.innerHTML = html;
  }
  
  highlightMatches(text, query) {
    if (!query) return text;
    
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }
  
  debounce(func, wait) {
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
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new EnhancedSearch();
});
```

### **Theme Switching**
Create `assets/js/theme-switcher.js`:
```javascript
class ThemeSwitcher {
  constructor() {
    this.themeToggle = document.getElementById('theme-toggle');
    this.currentTheme = localStorage.getItem('theme') || 'auto';
    
    this.init();
  }
  
  init() {
    this.applyTheme(this.currentTheme);
    this.setupEventListeners();
  }
  
  setupEventListeners() {
    this.themeToggle?.addEventListener('click', () => {
      this.toggleTheme();
    });
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (this.currentTheme === 'auto') {
        this.applySystemTheme();
      }
    });
  }
  
  toggleTheme() {
    const themes = ['light', 'dark', 'auto'];
    const currentIndex = themes.indexOf(this.currentTheme);
    const nextTheme = themes[(currentIndex + 1) % themes.length];
    
    this.setTheme(nextTheme);
  }
  
  setTheme(theme) {
    this.currentTheme = theme;
    localStorage.setItem('theme', theme);
    this.applyTheme(theme);
  }
  
  applyTheme(theme) {
    const html = document.documentElement;
    
    // Remove existing theme classes
    html.classList.remove('light', 'dark');
    
    if (theme === 'auto') {
      this.applySystemTheme();
    } else {
      html.classList.add(theme);
    }
    
    this.updateToggleIcon(theme);
  }
  
  applySystemTheme() {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.classList.toggle('dark', isDark);
  }
  
  updateToggleIcon(theme) {
    const sunIcon = this.themeToggle?.querySelector('.sun');
    const moonIcon = this.themeToggle?.querySelector('.moon');
    
    if (sunIcon && moonIcon) {
      sunIcon.style.display = theme === 'dark' ? 'block' : 'none';
      moonIcon.style.display = theme === 'light' ? 'block' : 'none';
    }
  }
}

// Initialize theme switcher
document.addEventListener('DOMContentLoaded', () => {
  new ThemeSwitcher();
});
```

## 📊 Analytics Integration

### **Google Analytics 4**
Add to `layouts/partials/extend_head.html`:
```html
{{- if hugo.IsProduction }}
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={{ site.Params.analytics.google.GA_MEASUREMENT_ID }}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '{{ site.Params.analytics.google.GA_MEASUREMENT_ID }}');
</script>
{{- end }}
```

### **Configuration**
```toml
[params.analytics]
  [params.analytics.google]
    GA_MEASUREMENT_ID = "G-XXXXXXXXXX"
```

## 🔒 Security Enhancements

### **Content Security Policy**
Add to `layouts/partials/extend_head.html`:
```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-inline' https://www.googletagmanager.com;
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
  img-src 'self' data: https:;
  font-src 'self' https://fonts.gstatic.com;
  connect-src 'self';
">
```

### **Additional Security Headers**
```html
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="DENY">
<meta http-equiv="X-XSS-Protection" content="1; mode=block">
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
```

---

**Next Steps**: Explore the [content authoring guide](content-guide.md) or check the [main README](../README.md) for deployment instructions.