# Content Authoring Guide

A comprehensive guide for creating and managing content on the Hugo personal blog.

## 📝 Content Creation Workflow

### Quick Start

```bash
# Create a new blog post
hugo new posts/my-awesome-post.md

# Create a new page
hugo new pages/about-me.md

# Start development server to preview
hugo server --buildDrafts
```

## 📋 Frontmatter Reference

### **Blog Posts** (`posts/`)

```yaml
---
title: "Your Post Title Here"
date: 2025-01-01T10:00:00Z
lastmod: 2025-01-01T12:00:00Z
draft: false
author: "Khairu Aqsara"
description: "A compelling description for SEO and social sharing (120-160 chars)"
summary: "Brief summary that appears in post lists"

# Categorization
tags: ["hugo", "web development", "tutorial"]
categories: ["tutorials", "technology"]

# SEO & Social
keywords: ["hugo", "static site", "web development"]
image: "/images/post-featured-image.jpg"

# Display Options  
featured: true
weight: 0
ShowToc: true
TocOpen: false
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
UseHugoToc: true

# Cover Image
cover:
    image: "/images/cover-image.jpg"
    alt: "Description of cover image"
    caption: "Optional caption for the image"
    relative: false
    hidden: false

# Edit Links
editPost:
    URL: "https://github.com/khairu-aqsara/khairu-aqsara.github.io/tree/main/content"
    Text: "Edit on GitHub"
    appendFilePath: true
---
```

### **Static Pages** (`pages/`)

```yaml
---
title: "Page Title"
description: "Page description for SEO"
date: 2025-01-01T00:00:00Z
draft: false
layout: "single"  # or custom layout
url: "/custom-url/"  # optional custom URL
---
```

### **Required Fields**

| Field | Description | Example |
|-------|-------------|---------|
| `title` | Post/page title (30-60 chars for SEO) | `"Hugo Best Practices"` |
| `date` | Publication date (ISO 8601 format) | `2025-01-01T10:00:00Z` |
| `draft` | Publication status | `false` (true = unpublished) |
| `description` | SEO meta description (120-160 chars) | `"Learn Hugo best practices..."` |

### **Optional Fields**

| Field | Purpose | Notes |
|-------|---------|--------|
| `lastmod` | Last modification date | Auto-updated with Git |
| `author` | Content author | Defaults to site author |
| `summary` | Custom excerpt | Auto-generated if omitted |
| `weight` | Sorting order | Lower = higher priority |
| `image` | Featured/social image | Used for Open Graph |

## ✍️ Writing Guidelines

### **Content Structure**

```markdown
# Main Title (H1) - Auto-generated from frontmatter

Brief introduction paragraph that hooks the reader and explains what they'll learn.

## Section Heading (H2)

Content for this section with proper paragraph spacing.

### Subsection (H3)

More detailed information. Keep hierarchy logical: H1 → H2 → H3 → H4.

#### Minor Subsection (H4)

Use H4 sparingly for very detailed breakdowns.

## Another Main Section

Continue with logical content flow...
```

### **Best Practices**

#### **Writing Style**
- **Clear and concise**: Write for scannable content
- **Active voice**: Preferred over passive voice
- **Personal tone**: Conversational but professional  
- **Code examples**: Include practical, working examples
- **Visual breaks**: Use headings, lists, and code blocks

#### **SEO Optimization**
- **Title length**: 30-60 characters for search results
- **Description**: 120-160 characters, compelling and descriptive
- **Keywords**: Natural integration, avoid keyword stuffing
- **Internal linking**: Link to related posts and pages
- **Image alt text**: Descriptive alternative text for images

#### **Content Length**
- **Blog posts**: Minimum 300 words for SEO value
- **Tutorials**: 800-2000 words with detailed examples
- **Technical guides**: As needed for complete coverage
- **Updates/news**: 150-500 words

## 🖼️ Images and Media

### **Image Management**

```markdown
# Using the responsive image shortcode
{{< responsive-image src="images/my-image.jpg" alt="Descriptive alt text" class="featured-image" >}}

# Standard markdown image
![Alt text](/images/my-image.jpg)

# Image with link
[![Alt text](/images/thumbnail.jpg)](/images/full-size.jpg)
```

### **Image Guidelines**

#### **File Organization**
```
static/images/
├── posts/
│   ├── 2025/
│   │   ├── post-name/
│   │   │   ├── featured.jpg
│   │   │   ├── screenshot-1.png
│   │   │   └── diagram.svg
├── pages/
│   ├── about-photo.jpg
│   └── contact-banner.png
└── general/
    ├── logo.png
    ├── favicon.ico
    └── social-preview.jpg
```

#### **Image Specifications**
- **Format**: WebP preferred, JPG/PNG fallback
- **Featured images**: 1200x630px (Open Graph ratio)
- **Content images**: Max 1200px width
- **File size**: <500KB per image, <200KB preferred
- **Alt text**: Descriptive, not redundant with caption

### **Responsive Images**

Use the custom shortcode for optimal performance:

```markdown
{{< responsive-image 
    src="images/posts/2025/tutorial/hero-image.jpg" 
    alt="Hugo tutorial setup screenshot showing terminal commands" 
    class="tutorial-image"
    loading="eager" >}}
```

This generates:
- Multiple image sizes (480px, 768px, 1200px)
- WebP format with fallbacks
- Proper `srcset` and `sizes` attributes
- Lazy loading by default

## 📝 Markdown Features

### **Code Blocks**

````markdown
```bash
# Bash commands with syntax highlighting
hugo new posts/my-post.md
hugo server --buildDrafts
```

```javascript
// JavaScript code example
function searchPosts(query) {
    return fuse.search(query);
}
```

```yaml
# YAML configuration
title: "My Post"
tags: ["hugo", "markdown"]
```
````

### **Lists and Tables**

```markdown
# Unordered list
- First item with **bold text**
- Second item with *italic text*
- Third item with `inline code`

# Ordered list
1. Step one with detailed explanation
2. Step two building on previous step
3. Step three completing the process

# Task list
- [x] Completed task
- [ ] Pending task
- [ ] Future task

# Table
| Feature | Status | Notes |
|---------|--------|--------|
| Search | ✅ Complete | Full-text search |
| SEO | ✅ Complete | 83.3% score |
| PWA | ✅ Complete | Service worker |
```

### **Links and References**

```markdown
# Internal links
[About page](/about/)
[Previous post](/posts/hugo-setup/)
[Search](/search/)

# External links
[Hugo documentation](https://gohugo.io/documentation/)
[GitHub repository](https://github.com/khairu-aqsara/khairu-aqsara.github.io)

# Reference-style links
This is [reference link][1] and [another reference][hugo-docs].

[1]: https://example.com
[hugo-docs]: https://gohugo.io/
```

### **Emphasis and Formatting**

```markdown
**Bold text** for strong emphasis
*Italic text* for subtle emphasis  
`Inline code` for technical terms
~~Strikethrough~~ for corrections

> Blockquote for important information
> or longer quotations from sources

---

Horizontal rule for section breaks
```

## 🏷️ Taxonomies (Tags & Categories)

### **Tagging Strategy**

#### **Categories** (High-level groupings)
- `tutorials` - Step-by-step guides
- `technology` - Tech discussions and reviews
- `personal` - Personal reflections and updates
- `projects` - Project showcases and development logs
- `resources` - Curated resources and tools

#### **Tags** (Specific topics)
- **Technical**: `hugo`, `javascript`, `python`, `docker`, `git`
- **Concepts**: `web-development`, `seo`, `performance`, `accessibility`
- **Formats**: `tutorial`, `guide`, `review`, `update`, `showcase`

### **Best Practices**
- **Categories**: 1-2 per post maximum
- **Tags**: 3-7 relevant tags per post
- **Consistency**: Use existing tags when possible
- **Specificity**: Balance between specific and discoverable
- **Lowercase**: Use kebab-case for multi-word tags

```yaml
# Good tagging example
categories: ["tutorials", "technology"]
tags: ["hugo", "static-site", "web-development", "performance", "seo"]

# Avoid over-tagging
tags: ["hugo", "static", "site", "generator", "web", "development", "tutorial", "guide", "blog", "cms"]
```

## 📅 Content Calendar

### **Publishing Schedule**
- **Regular posts**: 1-2 per week
- **Tutorial series**: Weekly installments
- **Project updates**: As needed
- **Resource roundups**: Monthly

### **Content Planning**

```yaml
# Draft tracking in frontmatter
draft: true
publish_date: "2025-02-01"
content_stage: "outline" # outline, draft, review, ready
estimated_reading_time: "10 minutes"
target_audience: "intermediate developers"
```

### **Seasonal Content**
- **Year-end**: Retrospectives and yearly summaries
- **New Year**: Goal setting and planning posts
- **Tech events**: Conference summaries and learnings
- **Tool updates**: Major version releases and changes

## 🔄 Content Updates

### **Maintenance Schedule**
- **Monthly**: Review and update older posts
- **Quarterly**: Check for broken links and outdated information
- **Annually**: Major content audits and archival decisions

### **Update Process**

```yaml
# Track updates in frontmatter
lastmod: 2025-01-15T10:00:00Z
update_reason: "Added new section on Hugo 0.115 features"
version: "1.1"
```

```markdown
<!-- Update notice in content -->
> **Update (January 2025)**: This post has been updated to reflect 
> changes in Hugo 0.115. The original concepts remain valid.
```

## 📊 Performance Guidelines

### **Content Optimization**
- **Reading level**: Aim for 8th-grade reading level
- **Paragraph length**: 2-4 sentences maximum
- **Sentence length**: Vary between 15-20 words average
- **Scannable**: Use headings, bullets, and visual breaks

### **Technical Performance**
- **Images**: Optimize before upload (<200KB preferred)
- **External links**: Use `rel="noopener"` for security
- **Code blocks**: Syntax highlighting improves readability
- **Internal linking**: Improve site navigation and SEO

### **SEO Content**
- **Focus keyword**: One primary keyword per post
- **Keyword density**: 1-2% natural integration
- **Meta description**: Write compelling, accurate descriptions
- **URL structure**: Use descriptive, keyword-rich slugs

## ✅ Content Checklist

### **Pre-Publication**
- [ ] **Frontmatter complete** with all required fields
- [ ] **Title optimized** (30-60 characters)
- [ ] **Description written** (120-160 characters)
- [ ] **Tags and categories** assigned appropriately
- [ ] **Images optimized** and alt text added
- [ ] **Links verified** (internal and external)
- [ ] **Spell check** completed
- [ ] **Reading flow** reviewed

### **Post-Publication**
- [ ] **Social sharing** tested (Twitter, LinkedIn, Facebook)
- [ ] **Mobile rendering** verified
- [ ] **Search functionality** confirmed (appears in site search)
- [ ] **Analytics** tracking confirmed
- [ ] **Feedback channels** monitored

### **Content Quality**
- [ ] **Value provided** to target audience
- [ ] **Actionable insights** included
- [ ] **Examples and code** tested and working
- [ ] **Logical structure** with clear headings
- [ ] **Conclusion** summarizes key points

---

**Need help?** Check the [theme customization guide](theme-customization.md) or [open an issue](https://github.com/khairu-aqsara/khairu-aqsara.github.io/issues) for support.