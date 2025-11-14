# GEMINI.md

## Project Overview

This is a personal blog created with [Jekyll](https://jekyllrb.com/) and the [Beautiful Jekyll](https://github.com/daattali/beautiful-jekyll) theme. The blog, titled "kuli-kode", features technical articles on software development, security, and related topics. The content is written in Markdown and includes code snippets and narrative-style posts.

## Building and Running

To work with this project locally, you need to have Ruby and Bundler installed.

- **Install dependencies:**

  ```bash
  bundle install
  ```

- **Run the development server:**

  ```bash
  bundle exec jekyll serve
  ```

  The site will be available at `http://localhost:4000`.

- **Build the site:**
  ```bash
  bundle exec jekyll build
  ```
  The static files will be generated in the `_site` directory.

## Development Conventions

- **Blog Posts:** New blog posts are created as Markdown files in the `_posts` directory. The filename format is `YYYY-MM-DD-title.md`.
- **Front Matter:** Each post must have YAML front matter at the top to define metadata such as `title`, `subtitle`, `date`, `categories`, and `tags`.
- **Static Assets:** Images, CSS, and JavaScript files are stored in the `assets` directory.
- **Configuration:** The main site configuration is in `_config.yml`.

## Key Files and Directories

- `_config.yml`: The main Jekyll configuration file. Contains settings for the site title, author, navigation links, social media, and more.
- `_posts/`: This directory contains all the blog posts as Markdown files.
- `assets/`: This directory holds static assets like images, CSS, and JavaScript.
- `aboutme.md`: The "About Me" page content.
- `index.html`: The main homepage layout.

## Usage

To add a new blog post:

1.  Create a new file in the `_posts` directory with the format `YYYY-MM-DD-your-post-title.md`.
2.  Add the YAML front matter to the top of the file with the necessary metadata.
3.  Write the post content in Markdown.
4.  Commit and push the changes to the GitHub repository. GitHub Pages will automatically build and deploy the new post.
5.  Always include emotional sense when writing the posts
6.  Always follow existing post pattern, so all post will have the same pattern like emotion aspect etc
7.  If you need to mention someone or there is a character in the post always use Devan, Myesha or Jovian as a main character or use all of them if needed
8.  each chapeter must be minimal has 2000 Words
9.  The post must always include example code from real case or scenario
10. It must be has minimum 5 Chapters
