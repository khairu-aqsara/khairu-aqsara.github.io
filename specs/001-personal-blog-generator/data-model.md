# Data Model: Hugo Personal Blog

## Content Entities

### Blog Post
**Location**: `/content/posts/*.md`
**Format**: Markdown with YAML/TOML frontmatter

**Frontmatter Fields**:
```yaml
title: "Post Title"                    # Required, string
date: "2025-01-19T10:00:00Z"          # Required, RFC3339 datetime
lastmod: "2025-01-19T15:30:00Z"       # Optional, auto-updated on changes
draft: false                           # Optional, boolean (default: false)
tags: ["hugo", "blogging", "tech"]     # Optional, array of strings
categories: ["technology"]             # Optional, array of strings  
description: "Brief post summary"      # Optional, string for SEO meta
slug: "custom-post-slug"               # Optional, string (auto-generated from title)
author: "Khairu Aqsara"               # Optional, string
featured: false                        # Optional, boolean for homepage featuring
weight: 0                             # Optional, integer for custom ordering
```

**Content Structure**:
- Markdown body with CommonMark compliance
- Support for code blocks with syntax highlighting
- Image references to `/static/images/` directory
- Internal links to other posts via Hugo's ref/relref shortcodes

**Validation Rules**:
- Title: 1-100 characters, no special markup
- Date: Must be valid RFC3339 format, not future-dated for published posts
- Draft: If true, excluded from production builds
- Tags: Maximum 10 tags per post, alphanumeric with hyphens/underscores
- Categories: Maximum 3 categories per post, lowercase with hyphens
- Slug: If provided, must be URL-safe (alphanumeric, hyphens only)

### Static Page
**Location**: `/content/pages/*.md`
**Format**: Markdown with simplified frontmatter

**Frontmatter Fields**:
```yaml
title: "Page Title"                    # Required, string
date: "2025-01-19T10:00:00Z"          # Required for ordering
draft: false                           # Optional, boolean
description: "Page description"        # Optional, string for SEO
menu: "main"                          # Optional, string for navigation menu
weight: 10                            # Optional, integer for menu ordering
```

**Special Pages**:
- `/content/about.md`: About page with author information
- `/content/_index.md`: Homepage content and configuration

### Site Configuration
**Location**: `/hugo.toml`
**Format**: TOML configuration

**Key Settings**:
```toml
baseURL = "https://username.github.io"
languageCode = "en-us"
title = "Site Title"
theme = "PaperMod"

[params]
  author = "Author Name"
  description = "Site description"
  
[params.social]
  github = "username"
  linkedin = "username"
  email = "email@example.com"

[taxonomies]
  tag = "tags"
  category = "categories"

[permalinks]
  posts = "/posts/:slug/"
```

## Hugo-Specific Entities

### Content Archetype
**Location**: `/archetypes/posts.md`
**Purpose**: Template for new post creation via `hugo new posts/example.md`

```yaml
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
tags: []
categories: []
description: ""
---

# {{ replace .Name "-" " " | title }}

Write your post content here...
```

### Theme Configuration
**Location**: Theme parameters in `hugo.toml`
**Purpose**: PaperMod theme customization

```toml
[params]
  # Site branding
  homeInfoParams.Title = "Welcome to My Blog"
  homeInfoParams.Content = "Personal documentation and technical insights"
  
  # Theme features
  ShowReadingTime = true
  ShowShareButtons = false
  ShowPostNavLinks = true
  ShowBreadCrumbs = true
  ShowCodeCopyButtons = true
  
  # Search functionality
  fuseOpts.includeScore = true
  fuseOpts.minMatchCharLength = 3
  fuseOpts.threshold = 0.5
```

### Asset Processing Pipeline
**Location**: `/assets/` directory
**Purpose**: Source files for Hugo Pipes processing

**CSS Assets**:
- `/assets/css/main.scss`: Main stylesheet
- `/assets/css/custom.scss`: Theme customizations
- Output: Minified, fingerprinted CSS in `/resources/`

**JavaScript Assets**:
- `/assets/js/search.js`: Client-side search functionality
- `/assets/js/theme.js`: Theme interactions
- Output: Minified, bundled JS in `/resources/`

### Search Index
**Location**: Generated at `/index.json`
**Purpose**: Client-side search data

**Structure**:
```json
[
  {
    "title": "Post Title",
    "content": "Post content excerpt...",
    "permalink": "/posts/post-slug/",
    "tags": ["tag1", "tag2"],
    "categories": ["category1"],
    "date": "2025-01-19"
  }
]
```

## Relationships

### Content Relationships
- **Posts → Tags**: Many-to-many via frontmatter array
- **Posts → Categories**: Many-to-many via frontmatter array  
- **Tags → Archive Pages**: One-to-one generated automatically
- **Categories → Archive Pages**: One-to-one generated automatically
- **Posts → Search Index**: All published posts included in JSON index

### URL Structure
- **Homepage**: `/` (paginated post list)
- **Posts**: `/posts/{slug}/` (individual post pages)
- **Tag Archives**: `/tags/{tag}/` (paginated post list by tag)
- **Category Archives**: `/categories/{category}/` (paginated post list by category)
- **Date Archives**: `/posts/{year}/` and `/posts/{year}/{month}/` (paginated by date)
- **Static Pages**: `/{slug}/` (about, contact, etc.)
- **RSS Feeds**: `/index.xml`, `/tags/{tag}/index.xml`, `/categories/{category}/index.xml`

## State Transitions

### Post Lifecycle
```
1. Creation → Draft state (draft: true)
2. Writing → Draft state (content development)
3. Review → Draft state (self-review process)
4. Publication → Published state (draft: false or removed)
5. Updates → Published state (lastmod updated)
6. Archive → Published state (remains accessible)
```

### Build Process States
```
1. Content Change → Trigger build
2. Hugo Processing → Parse frontmatter, render Markdown
3. Asset Processing → Minify CSS/JS via Hugo Pipes
4. Site Generation → Create HTML pages, search index, feeds
5. Deployment → Upload to GitHub Pages
6. Live Site → Accessible to visitors
```

## Validation Rules

### Content Validation
- All posts must have valid frontmatter (YAML/TOML syntax)
- Required fields: title, date
- Date format: RFC3339 compliant
- No future dates for published posts (draft: false)
- Tags and categories: lowercase, URL-safe characters only

### Build Validation  
- All internal links must resolve to existing content
- All image references must exist in `/static/` directory
- Hugo build must complete without errors
- Generated HTML must be valid and accessible
- Asset pipeline must produce optimized outputs

### Deployment Validation
- GitHub Pages compatibility check
- All assets served with correct MIME types
- RSS feeds validate against standards
- Site loads correctly with JavaScript disabled
- Mobile responsiveness verified