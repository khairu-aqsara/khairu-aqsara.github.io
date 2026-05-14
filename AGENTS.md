# AGENTS.md — kuli-kode

Personal blog built with **Jekyll + Beautiful Jekyll theme** (v6.0.1).  
Deployed via **GitHub Pages** at `kulikode.is-a.dev` (custom domain in `CNAME`).  
CI runs on push/PR to `main` — see `.github/workflows/ci.yml`.

## Commands

```bash
bundle install                        # install Ruby deps
bundle exec jekyll serve              # dev server at localhost:4000
bundle exec jekyll build              # build to _site/
bundle exec appraisal jekyll build --future --config _config_ci.yml,_config.yml  # CI build
```

## Post conventions

All posts live in `_posts/` as `YYYY-MM-DD-title.md`. Required:

- **Language**: Casual Bahasa Indonesia ("chat style")
- **Length**: minimum 5 chapters, minimum 2000 words per post
- **Code**: must include real code examples from actual scenarios
- **Characters** (treat them as siblings — 3 main characters):
  - Myesha (she, big sister)
  - Devan (he, middle)
  - Jovian (he, youngest brother)
- **Cities** you may reference: Yogyakarta, Berbah, Takengon, Krui, Bener Meriah, Pante Raya, Sleman
- **Emotional sense**: always include emotional/narrative depth
- Follow existing post patterns (each post has the same emotional/structure template)

## Key config

- `_config.yml`: site title, navbar, colors, timezone `Asia/Jakarta`, paginate (5), kramdown/GFM
- `assets/css/custom-styles.css`: custom fonts (Copernicus body, StyreneA headings)

## Existing instruction files

- `GEMINI.md` — detailed post-writing rules (character names, language style, minimums, city list). An agent writing posts **must** read this.

## Structure

| Path | Purpose |
|---|---|
| `_posts/` | Blog posts (Markdown) |
| `_layouts/` | Jekyll layouts (base, default, home, minimal, page, post) |
| `_includes/` | Reusable template fragments |
| `assets/` | CSS, JS, fonts, images |
| `_data/ui-text.yml` | UI text translations |
| `aboutme.md` | About page |
| `index.html` | Homepage (layout: home) |
