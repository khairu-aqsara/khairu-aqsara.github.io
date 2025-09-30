# Quickstart Guide: Hugo Personal Blog

This guide provides step-by-step instructions to set up and deploy the Hugo personal blog from scratch to production.

## Prerequisites

- [ ] Hugo Extended >= 0.115 installed locally
- [ ] Git installed and configured  
- [ ] GitHub account with repository access
- [ ] Basic familiarity with Markdown and command line

## Quick Setup (15 minutes)

### 1. Initialize Hugo Site
```bash
# Create new Hugo site in current directory
hugo new site . --force

# Verify Hugo installation and version
hugo version
```

**Expected Result**: Hugo site structure created with `config.toml`, `content/`, `layouts/`, etc.

### 2. Add PaperMod Theme
```bash
# Add PaperMod as git submodule
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod

# Update git modules
git submodule update --init --recursive
```

**Expected Result**: PaperMod theme downloaded to `themes/PaperMod/` directory.

### 3. Configure Site
```bash
# Replace default config with our configuration
cp specs/001-personal-blog-generator/contracts/hugo-config.toml hugo.toml

# Create content directories
mkdir -p content/posts
mkdir -p content/pages
mkdir -p static/images
mkdir -p assets/css
mkdir -p assets/js
```

**Expected Result**: Site configured with proper settings, directories created.

### 4. Set Up Content Archetypes
```bash
# Copy post archetype template
cp specs/001-personal-blog-generator/contracts/post-archetype.md archetypes/posts.md

# Create default archetype
cat > archetypes/default.md << 'EOF'
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
---
EOF
```

**Expected Result**: Content templates ready for `hugo new` command.

### 5. Create Initial Content
```bash
# Create about page
hugo new pages/about.md

# Create first blog post
hugo new posts/welcome-to-my-blog.md

# Create homepage content
cat > content/_index.md << 'EOF'
---
title: "Home"
---
EOF
```

**Expected Result**: Sample content created for testing.

### 6. Test Local Development
```bash
# Start Hugo development server
hugo server --buildDrafts --buildFuture

# Open browser to http://localhost:1313
# Verify site loads correctly with theme
```

**Expected Result**: 
- Site accessible at localhost:1313
- PaperMod theme active
- Navigation menu functional
- Sample content visible

### 7. Set Up GitHub Actions
```bash
# Create GitHub Actions workflow
mkdir -p .github/workflows
cp specs/001-personal-blog-generator/contracts/github-actions-workflow.yml .github/workflows/hugo.yml

# Configure GitHub Pages in repository settings
# Settings > Pages > Source: GitHub Actions
```

**Expected Result**: Automated deployment configured for pushes to main branch.

### 8. Deploy to Production
```bash
# Commit all changes
git add .
git commit -m "Initial Hugo blog setup with PaperMod theme"

# Push to GitHub (triggers deployment)
git push origin main

# Verify deployment in Actions tab
# Check site at https://username.github.io
```

**Expected Result**: 
- GitHub Actions workflow runs successfully
- Site deployed to GitHub Pages
- Production site accessible and functional

## Verification Checklist

### Local Development ✅
- [ ] `hugo server` starts without errors
- [ ] Site loads at localhost:1313
- [ ] Theme applied correctly (PaperMod)
- [ ] Navigation menu works
- [ ] About page accessible
- [ ] Blog posts list on homepage
- [ ] Dark/light theme toggle functional

### Content Creation ✅
- [ ] `hugo new posts/test.md` creates properly formatted post
- [ ] Frontmatter populated from archetype
- [ ] Draft posts visible in development mode
- [ ] Published posts (draft: false) appear on site
- [ ] Tags and categories functional

### Asset Processing ✅
- [ ] CSS minified in production build
- [ ] JavaScript bundled correctly
- [ ] Images served from /static/ directory
- [ ] Hugo Pipes processing works for assets
- [ ] Fingerprinting applied to assets

### Production Deployment ✅
- [ ] GitHub Actions workflow completes successfully
- [ ] Site accessible at GitHub Pages URL
- [ ] All pages load correctly
- [ ] Images and assets load properly
- [ ] RSS feed accessible (/index.xml)
- [ ] Search functionality works
- [ ] Mobile responsive design

### SEO & Accessibility ✅
- [ ] Meta tags present in HTML head
- [ ] Open Graph data included
- [ ] Sitemap.xml generated
- [ ] Robots.txt present
- [ ] Heading hierarchy proper (h1 → h6)
- [ ] Alt text on images
- [ ] Color contrast acceptable

## Common Troubleshooting

### Hugo Server Issues
```bash
# Clear Hugo cache and restart
hugo mod clean --all
rm -rf resources/ public/
hugo server --buildDrafts
```

### Theme Problems
```bash
# Update theme to latest version
cd themes/PaperMod
git pull origin master
cd ../..
```

### Build Failures
```bash
# Check Hugo version compatibility
hugo version

# Validate configuration
hugo config

# Check for content errors
hugo --buildDrafts --verbose
```

### GitHub Actions Failures
- Verify Hugo version in workflow matches local
- Check repository permissions for GitHub Pages
- Ensure submodules properly configured
- Review Actions logs for specific errors

## Next Steps

After successful setup:

1. **Customize Content**: Edit about page, create first real blog post
2. **Theme Customization**: Modify colors, fonts, layout in theme parameters
3. **Content Strategy**: Plan content calendar and post topics
4. **SEO Optimization**: Add analytics, optimize meta descriptions
5. **Performance**: Monitor Core Web Vitals, optimize images
6. **Backup**: Set up content backup strategy and version control workflow

## Support Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [PaperMod Theme Guide](https://github.com/adityatelange/hugo-PaperMod)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Markdown Guide](https://www.markdownguide.org/)

---
*Estimated completion time: 15-30 minutes for experienced developers, 45-60 minutes for beginners.*