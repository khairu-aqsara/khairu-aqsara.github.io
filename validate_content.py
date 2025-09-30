#!/usr/bin/env python3
"""
Content Validation & Testing Script for Hugo Blog
Phase 3.9 Implementation
"""

import os
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
import yaml
import glob
import subprocess
from datetime import datetime

class ContentValidator:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.content_dir = self.root_dir / "content"
        self.public_dir = self.root_dir / "public"
        self.errors = []
        self.warnings = []
        self.info = []
        
    def log_error(self, message):
        """Log validation error"""
        self.errors.append(f"❌ ERROR: {message}")
        
    def log_warning(self, message):
        """Log validation warning"""
        self.warnings.append(f"⚠️  WARNING: {message}")
        
    def log_info(self, message):
        """Log validation info"""
        self.info.append(f"ℹ️  INFO: {message}")
        
    def validate_frontmatter(self):
        """Validate frontmatter in all markdown files"""
        print("🔍 Validating frontmatter...")
        
        required_fields = ["title"]
        recommended_fields = ["description", "date"]
        
        for md_file in self.content_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract frontmatter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter_content = parts[1].strip()
                        try:
                            frontmatter = yaml.safe_load(frontmatter_content)
                        except yaml.YAMLError as e:
                            self.log_error(f"Invalid YAML frontmatter in {md_file}: {e}")
                            continue
                    else:
                        self.log_error(f"Malformed frontmatter in {md_file}")
                        continue
                else:
                    self.log_warning(f"No frontmatter found in {md_file}")
                    continue
                
                # Check required fields
                for field in required_fields:
                    if field not in frontmatter or not frontmatter[field]:
                        self.log_error(f"Missing required field '{field}' in {md_file}")
                
                # Check recommended fields
                for field in recommended_fields:
                    if field not in frontmatter:
                        self.log_warning(f"Missing recommended field '{field}' in {md_file}")
                
                # Validate specific fields
                if 'draft' in frontmatter and frontmatter['draft']:
                    self.log_info(f"Draft content found: {md_file}")
                
                if 'date' in frontmatter:
                    try:
                        # Try to parse the date
                        if isinstance(frontmatter['date'], str):
                            datetime.fromisoformat(frontmatter['date'].replace('Z', '+00:00'))
                    except (ValueError, TypeError):
                        self.log_warning(f"Invalid date format in {md_file}: {frontmatter['date']}")
                
            except Exception as e:
                self.log_error(f"Error processing {md_file}: {e}")
    
    def validate_content_structure(self):
        """Validate content structure and organization"""
        print("🔍 Validating content structure...")
        
        # Check for required content files
        required_files = [
            "content/_index.md",
            "content/search.md"
        ]
        
        for req_file in required_files:
            file_path = self.root_dir / req_file
            if not file_path.exists():
                self.log_error(f"Required file missing: {req_file}")
            else:
                self.log_info(f"Required file exists: {req_file}")
        
        # Check content organization
        posts_dir = self.content_dir / "posts"
        pages_dir = self.content_dir / "pages"
        
        if posts_dir.exists():
            post_count = len(list(posts_dir.glob("*.md")))
            self.log_info(f"Found {post_count} blog posts")
        else:
            self.log_warning("No posts directory found")
            
        if pages_dir.exists():
            page_count = len(list(pages_dir.glob("*.md")))
            self.log_info(f"Found {page_count} static pages")
        
    def validate_markdown_syntax(self):
        """Validate markdown syntax and formatting"""
        print("🔍 Validating markdown syntax...")
        
        for md_file in self.content_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for common markdown issues
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    # Check for unescaped special characters
                    if re.search(r'[<>](?![a-zA-Z/])', line):
                        self.log_warning(f"Potential unescaped HTML chars in {md_file}:{i}")
                    
                    # Check for malformed links
                    if '[' in line and ']' in line and '(' in line and ')' in line:
                        if not re.search(r'\[.*\]\(.*\)', line):
                            self.log_warning(f"Potential malformed link in {md_file}:{i}")
                
                # Check for proper heading hierarchy
                headings = re.findall(r'^(#+)\s+(.+)$', content, re.MULTILINE)
                prev_level = 0
                for heading in headings:
                    current_level = len(heading[0])
                    if current_level > prev_level + 1:
                        self.log_warning(f"Heading hierarchy skip in {md_file}: {heading[1]}")
                    prev_level = current_level
                    
            except Exception as e:
                self.log_error(f"Error validating markdown in {md_file}: {e}")
    
    def validate_generated_site(self):
        """Validate the generated Hugo site"""
        print("🔍 Validating generated site...")
        
        if not self.public_dir.exists():
            self.log_error("Public directory not found. Run 'hugo' to build the site first.")
            return
        
        # Check essential files
        essential_files = [
            "public/index.html",
            "public/sitemap.xml",
            "public/robots.txt",
            "public/index.xml",  # RSS feed
            "public/index.json"  # Search index
        ]
        
        for file_path in essential_files:
            full_path = self.root_dir / file_path
            if not full_path.exists():
                self.log_error(f"Essential file missing: {file_path}")
            else:
                self.log_info(f"Essential file exists: {file_path}")
                
                # Validate file size
                file_size = full_path.stat().st_size
                if file_size == 0:
                    self.log_error(f"Essential file is empty: {file_path}")
                else:
                    self.log_info(f"File size OK: {file_path} ({file_size} bytes)")
    
    def validate_search_functionality(self):
        """Validate search functionality"""
        print("🔍 Validating search functionality...")
        
        search_index_path = self.public_dir / "index.json"
        search_page_path = self.public_dir / "search" / "index.html"
        
        # Validate search index
        if search_index_path.exists():
            try:
                with open(search_index_path, 'r', encoding='utf-8') as f:
                    search_data = json.load(f)
                
                if isinstance(search_data, list):
                    self.log_info(f"Search index valid with {len(search_data)} entries")
                    
                    # Validate search entries structure
                    required_keys = ["title", "content", "permalink", "summary"]
                    for i, entry in enumerate(search_data[:3]):  # Check first 3 entries
                        for key in required_keys:
                            if key not in entry:
                                self.log_error(f"Search entry {i} missing key: {key}")
                else:
                    self.log_error("Search index is not a valid array")
                    
            except json.JSONDecodeError as e:
                self.log_error(f"Invalid JSON in search index: {e}")
        else:
            self.log_error("Search index file not found")
        
        # Validate search page
        if search_page_path.exists():
            with open(search_page_path, 'r', encoding='utf-8') as f:
                search_html = f.read()
            
            # Check for search elements
            if re.search(r'id\s*=\s*["\']?searchInput["\']?', search_html):
                self.log_info("Search input element found")
            else:
                self.log_error("Search input element not found")
                
            if re.search(r'id\s*=\s*["\']?searchResults["\']?', search_html):
                self.log_info("Search results element found")
            else:
                self.log_error("Search results element not found")
        else:
            self.log_error("Search page not found")
    
    def validate_links_and_assets(self):
        """Validate internal links and assets"""
        print("🔍 Validating links and assets...")
        
        # Check for broken internal links in HTML files
        html_files = list(self.public_dir.rglob("*.html"))
        self.log_info(f"Checking {len(html_files)} HTML files for broken links")
        
        for html_file in html_files[:10]:  # Limit to first 10 for performance
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find internal links
                internal_links = re.findall(r'href=["\']([^"\']*)["\']', content)
                for link in internal_links:
                    if link.startswith('/') and not link.startswith('//'):
                        # Internal absolute link
                        target_path = self.public_dir / link.lstrip('/')
                        if not target_path.exists() and not (target_path.parent / "index.html").exists():
                            self.log_warning(f"Potential broken internal link in {html_file}: {link}")
                            
            except Exception as e:
                self.log_warning(f"Error checking links in {html_file}: {e}")
    
    def validate_seo_elements(self):
        """Validate SEO elements"""
        print("🔍 Validating SEO elements...")
        
        index_html = self.public_dir / "index.html"
        if index_html.exists():
            with open(index_html, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for essential SEO elements
            seo_checks = {
                'title': r'<title>[^<]+</title>',
                'meta description': r'<meta[^>]*name=["\']description["\'][^>]*>',
                'meta viewport': r'<meta[^>]*name=["\']viewport["\'][^>]*>',
                'canonical URL': r'<link[^>]*rel=["\']canonical["\'][^>]*>',
                'Open Graph': r'<meta[^>]*property=["\']og:',
            }
            
            for check_name, pattern in seo_checks.items():
                if re.search(pattern, content, re.IGNORECASE):
                    self.log_info(f"SEO element found: {check_name}")
                else:
                    self.log_warning(f"SEO element missing: {check_name}")
        
        # Check robots.txt
        robots_path = self.public_dir / "robots.txt"
        if robots_path.exists():
            with open(robots_path, 'r', encoding='utf-8') as f:
                robots_content = f.read()
            
            if 'Sitemap:' in robots_content:
                self.log_info("Sitemap reference found in robots.txt")
            else:
                self.log_warning("No sitemap reference in robots.txt")
        
    def run_hugo_validation(self):
        """Run Hugo's built-in validation"""
        print("🔍 Running Hugo validation...")
        
        try:
            # Run hugo check for internal consistency
            result = subprocess.run(['hugo', '--printUnusedTemplates'], 
                                 capture_output=True, text=True, cwd=self.root_dir)
            
            if result.returncode == 0:
                self.log_info("Hugo build completed successfully")
            else:
                self.log_error(f"Hugo build failed: {result.stderr}")
                
        except FileNotFoundError:
            self.log_warning("Hugo command not found - skipping Hugo validation")
        except Exception as e:
            self.log_warning(f"Error running Hugo validation: {e}")
    
    def generate_report(self):
        """Generate validation report"""
        print("\n" + "="*60)
        print("CONTENT VALIDATION & TESTING REPORT")
        print("="*60)
        
        # Summary
        total_issues = len(self.errors) + len(self.warnings)
        print(f"\nSummary:")
        print(f"  ✅ Info messages: {len(self.info)}")
        print(f"  ⚠️  Warnings: {len(self.warnings)}")
        print(f"  ❌ Errors: {len(self.errors)}")
        print(f"  📊 Total issues: {total_issues}")
        
        # Detailed results
        if self.info:
            print(f"\n📋 Information ({len(self.info)}):")
            for msg in self.info:
                print(f"  {msg}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for msg in self.warnings:
                print(f"  {msg}")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for msg in self.errors:
                print(f"  {msg}")
        
        # Status
        print(f"\n{'='*60}")
        if self.errors:
            print("🔴 VALIDATION FAILED - Errors found that need fixing")
            return False
        elif self.warnings:
            print("🟡 VALIDATION PASSED WITH WARNINGS - Consider addressing warnings")
            return True
        else:
            print("🟢 VALIDATION PASSED - All checks completed successfully")
            return True
    
    def run_all_validations(self):
        """Run all validation tests"""
        print("🚀 Starting Content Validation & Testing...")
        print(f"📁 Root directory: {self.root_dir.absolute()}")
        
        self.validate_frontmatter()
        self.validate_content_structure()
        self.validate_markdown_syntax()
        self.validate_generated_site()
        self.validate_search_functionality()
        self.validate_links_and_assets()
        self.validate_seo_elements()
        self.run_hugo_validation()
        
        return self.generate_report()

def main():
    """Main execution function"""
    validator = ContentValidator()
    success = validator.run_all_validations()
    
    # Save detailed report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"validation_report_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("HUGO BLOG CONTENT VALIDATION REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        
        f.write("INFORMATION:\n")
        for msg in validator.info:
            f.write(f"{msg}\n")
        
        f.write(f"\nWARNINGS:\n")
        for msg in validator.warnings:
            f.write(f"{msg}\n")
        
        f.write(f"\nERRORS:\n")
        for msg in validator.errors:
            f.write(f"{msg}\n")
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()