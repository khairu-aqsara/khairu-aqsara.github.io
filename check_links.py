#!/usr/bin/env python3
"""
Link Checker for Hugo Site
Phase 3.9: Content Validation & Testing
"""

import re
import os
from pathlib import Path
from urllib.parse import urljoin, urlparse
import json

class LinkChecker:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.public_dir = self.root_dir / "public"
        self.base_url = "https://khairu-aqsara.github.io"
        self.internal_links = set()
        self.external_links = set()
        self.broken_links = []
        self.warnings = []
        
    def extract_links_from_html(self, html_content, source_file):
        """Extract all links from HTML content"""
        # Find href attributes
        href_pattern = r'href=["\']([^"\']*)["\']'
        src_pattern = r'src=["\']([^"\']*)["\']'
        
        links = []
        
        # Extract href links
        for match in re.finditer(href_pattern, html_content, re.IGNORECASE):
            url = match.group(1)
            if url and not url.startswith('#') and not url.startswith('mailto:'):
                links.append(('href', url))
        
        # Extract src links (images, scripts)
        for match in re.finditer(src_pattern, html_content, re.IGNORECASE):
            url = match.group(1)
            if url and not url.startswith('data:'):
                links.append(('src', url))
        
        return links
    
    def classify_link(self, url):
        """Classify link as internal, external, or asset"""
        if url.startswith('http://') or url.startswith('https://'):
            if self.base_url in url:
                return 'internal_absolute'
            else:
                return 'external'
        elif url.startswith('//'):
            return 'external'
        elif url.startswith('/'):
            return 'internal_root'
        else:
            return 'internal_relative'
    
    def check_internal_link(self, url, source_file):
        """Check if internal link exists"""
        if url.startswith('/'):
            # Root-relative link
            target_path = self.public_dir / url.lstrip('/')
        else:
            # Relative link
            source_dir = source_file.parent
            target_path = source_dir / url
        
        # Try exact path first
        if target_path.exists():
            return True
        
        # Try with index.html
        if target_path.is_dir():
            index_path = target_path / "index.html"
            if index_path.exists():
                return True
        
        # Try adding index.html to path
        index_path = target_path / "index.html"
        if index_path.exists():
            return True
        
        # Try without trailing slash
        if str(target_path).endswith('/'):
            no_slash_path = Path(str(target_path).rstrip('/'))
            if no_slash_path.exists():
                return True
            index_path = no_slash_path / "index.html"
            if index_path.exists():
                return True
        
        return False
    
    def check_asset_link(self, url, source_file):
        """Check if asset link exists"""
        if url.startswith('/'):
            asset_path = self.public_dir / url.lstrip('/')
        else:
            source_dir = source_file.parent
            asset_path = source_dir / url
        
        return asset_path.exists()
    
    def scan_html_files(self):
        """Scan all HTML files for links"""
        print("🔍 Scanning HTML files for links...")
        
        html_files = list(self.public_dir.rglob("*.html"))
        print(f"Found {len(html_files)} HTML files to check")
        
        total_links = 0
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                links = self.extract_links_from_html(content, html_file)
                total_links += len(links)
                
                for link_type, url in links:
                    link_classification = self.classify_link(url)
                    
                    if link_classification == 'external':
                        self.external_links.add(url)
                    elif link_classification in ['internal_absolute', 'internal_root', 'internal_relative']:
                        self.internal_links.add(url)
                        
                        # Check internal links
                        if link_type == 'href':
                            if not self.check_internal_link(url, html_file):
                                self.broken_links.append({
                                    'file': str(html_file.relative_to(self.public_dir)),
                                    'url': url,
                                    'type': 'internal_link'
                                })
                        elif link_type == 'src':
                            if not self.check_asset_link(url, html_file):
                                self.broken_links.append({
                                    'file': str(html_file.relative_to(self.public_dir)),
                                    'url': url,
                                    'type': 'asset'
                                })
                                
            except Exception as e:
                self.warnings.append(f"Error processing {html_file}: {e}")
        
        print(f"Scanned {total_links} total links")
        print(f"Found {len(self.internal_links)} internal links")
        print(f"Found {len(self.external_links)} external links")
    
    def check_important_pages(self):
        """Check that important pages exist and are linked"""
        print("📄 Checking important pages...")
        
        important_pages = {
            '/': 'Homepage',
            '/posts/': 'Posts page',
            '/search/': 'Search page',
            '/about/': 'About page',
            '/tags/': 'Tags page',
            '/sitemap.xml': 'Sitemap',
            '/robots.txt': 'Robots.txt'
        }
        
        for url, description in important_pages.items():
            if url.endswith('.xml') or url.endswith('.txt'):
                # Check file existence
                file_path = self.public_dir / url.lstrip('/')
                if not file_path.exists():
                    self.broken_links.append({
                        'file': 'site_structure',
                        'url': url,
                        'type': 'missing_important_file'
                    })
            else:
                # Check page existence
                if not self.check_internal_link(url, self.public_dir):
                    self.broken_links.append({
                        'file': 'site_structure', 
                        'url': url,
                        'type': 'missing_important_page'
                    })
    
    def generate_report(self):
        """Generate link checking report"""
        print("\n" + "="*60)
        print("🔗 LINK CHECKING REPORT")
        print("="*60)
        
        print(f"\n📊 Summary:")
        print(f"  🔗 Internal links: {len(self.internal_links)}")
        print(f"  🌐 External links: {len(self.external_links)}")
        print(f"  ❌ Broken links: {len(self.broken_links)}")
        print(f"  ⚠️  Warnings: {len(self.warnings)}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.broken_links:
            print(f"\n❌ Broken Links ({len(self.broken_links)}):")
            
            # Group by type
            by_type = {}
            for link in self.broken_links:
                link_type = link['type']
                if link_type not in by_type:
                    by_type[link_type] = []
                by_type[link_type].append(link)
            
            for link_type, links in by_type.items():
                print(f"\n  {link_type.replace('_', ' ').title()}:")
                for link in links:
                    print(f"    📄 {link['file']} → {link['url']}")
        
        if not self.broken_links and not self.warnings:
            print("\n🎉 All links are valid!")
        
        # Save detailed report
        report_data = {
            'summary': {
                'internal_links': len(self.internal_links),
                'external_links': len(self.external_links), 
                'broken_links': len(self.broken_links),
                'warnings': len(self.warnings)
            },
            'internal_links': sorted(list(self.internal_links)),
            'external_links': sorted(list(self.external_links)),
            'broken_links': self.broken_links,
            'warnings': self.warnings
        }
        
        with open('link_check_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: link_check_report.json")
        
        return len(self.broken_links) == 0
    
    def run_check(self):
        """Run complete link check"""
        print("🚀 Starting link checking...")
        
        if not self.public_dir.exists():
            print("❌ Public directory not found. Run 'hugo' to build the site first.")
            return False
        
        self.scan_html_files()
        self.check_important_pages()
        
        return self.generate_report()

def main():
    """Main execution"""
    checker = LinkChecker()
    success = checker.run_check()
    
    if success:
        print("\n✅ Link check passed!")
        exit(0)
    else:
        print("\n❌ Link check failed - broken links found")
        exit(1)

if __name__ == "__main__":
    main()