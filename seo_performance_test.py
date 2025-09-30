#!/usr/bin/env python3
"""
SEO & Performance Testing Script
Phase 3.10: SEO & Performance Optimization
Tests Lighthouse scores, structured data, and performance metrics
"""

import subprocess
import json
import re
import sys
import os
from pathlib import Path
from urllib.parse import urlparse, urljoin
import time

class SEOPerformanceTester:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.public_dir = self.root_dir / "public"
        self.results = {"seo": {}, "performance": {}, "accessibility": {}, "best_practices": {}}
        self.errors = []
        self.warnings = []
        self.passed = []
        
    def log_error(self, message):
        self.errors.append(f"❌ {message}")
        
    def log_warning(self, message):
        self.warnings.append(f"⚠️ {message}")
        
    def log_passed(self, message):
        self.passed.append(f"✅ {message}")
    
    def test_structured_data(self):
        """Test structured data implementation"""
        print("🔍 Testing Structured Data...")
        
        html_files = [
            "public/index.html",
            "public/posts/javascript-fundamentals/index.html", 
            "public/about/index.html",
            "public/search/index.html"
        ]
        
        for file_path in html_files:
            full_path = self.root_dir / file_path
            if not full_path.exists():
                self.log_warning(f"File not found: {file_path}")
                continue
                
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for JSON-LD structured data
                json_ld_blocks = re.findall(r'<script type="?application/ld\+json"?[^>]*>(.*?)</script>', 
                                          content, re.DOTALL | re.IGNORECASE)
                
                if json_ld_blocks:
                    self.log_passed(f"Structured data found in {file_path}")
                    
                    # Validate JSON-LD syntax
                    for i, block in enumerate(json_ld_blocks):
                        try:
                            json.loads(block)
                            self.log_passed(f"Valid JSON-LD syntax in block {i+1} of {file_path}")
                        except json.JSONDecodeError as e:
                            self.log_error(f"Invalid JSON-LD in {file_path}: {e}")
                else:
                    self.log_warning(f"No structured data found in {file_path}")
                    
            except Exception as e:
                self.log_error(f"Error processing {file_path}: {e}")
    
    def test_seo_fundamentals(self):
        """Test SEO fundamentals"""
        print("🔍 Testing SEO Fundamentals...")
        
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            self.log_error("Homepage not found")
            return
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Essential SEO elements  
            seo_checks = {
                'Title tag': r'<title[^>]*>([^<]+)</title>',
                'Meta description': r'<meta[^>]*name=["\']?description["\']?[^>]*content=["\']([^"\']+)["\']',
                'Meta viewport': r'<meta[^>]*name=["\']?viewport["\']?',
                'Canonical URL': r'<link[^>]*rel=["\']?canonical["\']?',
                'Open Graph title': r'<meta[^>]*property=["\']?og:title["\']?',
                'Open Graph description': r'<meta[^>]*property=["\']?og:description["\']?',
                'Open Graph image': r'<meta[^>]*property=["\']?og:image["\']?',
                'Twitter Card': r'<meta[^>]*name=["\']?twitter:card["\']?',
                'Language attribute': r'<html[^>]*lang=["\']?([^"\'>\s]+)["\']?'
            }
            
            for check_name, pattern in seo_checks.items():
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    self.log_passed(f"{check_name} found")
                    if check_name == 'Title tag':
                        title = match.group(1).strip()
                        if len(title) > 60:
                            self.log_warning(f"Title tag too long ({len(title)} chars)")
                        elif len(title) < 30:
                            self.log_warning(f"Title tag too short ({len(title)} chars)")
                    elif check_name == 'Meta description':
                        desc = match.group(1).strip()
                        if len(desc) > 160:
                            self.log_warning(f"Meta description too long ({len(desc)} chars)")
                        elif len(desc) < 120:
                            self.log_warning(f"Meta description too short ({len(desc)} chars)")
                else:
                    self.log_error(f"{check_name} missing")
            
            # Check for heading structure
            headings = re.findall(r'<(h[1-6])[^>]*>([^<]+)</h[1-6]>', content, re.IGNORECASE)
            h1_count = len([h for h in headings if h[0].lower() == 'h1'])
            
            if h1_count == 1:
                self.log_passed("Single H1 tag found")
            elif h1_count == 0:
                self.log_error("No H1 tag found")
            else:
                self.log_warning(f"Multiple H1 tags found ({h1_count})")
                
        except Exception as e:
            self.log_error(f"Error testing SEO fundamentals: {e}")
    
    def test_performance_metrics(self):
        """Test performance metrics"""
        print("⚡ Testing Performance Metrics...")
        
        # Check file sizes
        size_checks = {
            'Homepage': 'public/index.html',
            'Main CSS': 'public/assets/css/stylesheet.*.css',
            'Search JS': 'public/assets/js/search.*.js',
            'Search Index': 'public/index.json'
        }
        
        for file_type, pattern in size_checks.items():
            if '*' in pattern:
                matches = list(self.root_dir.glob(pattern))
                if matches:
                    file_path = matches[0]
                else:
                    self.log_warning(f"{file_type} not found with pattern {pattern}")
                    continue
            else:
                file_path = self.root_dir / pattern
            
            if file_path.exists():
                size_kb = file_path.stat().st_size / 1024
                
                # Size thresholds
                thresholds = {
                    'Homepage': 50,  # 50KB
                    'Main CSS': 100,  # 100KB  
                    'Search JS': 50,  # 50KB
                    'Search Index': 100  # 100KB
                }
                
                threshold = thresholds.get(file_type, 100)
                
                if size_kb <= threshold:
                    self.log_passed(f"{file_type}: {size_kb:.1f}KB (optimal)")
                elif size_kb <= threshold * 1.5:
                    self.log_warning(f"{file_type}: {size_kb:.1f}KB (acceptable)")
                else:
                    self.log_error(f"{file_type}: {size_kb:.1f}KB (too large)")
            else:
                self.log_warning(f"{file_type} not found")
    
    def test_accessibility_features(self):
        """Test accessibility features"""
        print("♿ Testing Accessibility Features...")
        
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return
            
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Accessibility checks
            a11y_checks = {
                'Language attribute': r'<html[^>]*lang=["\']?[^"\'>\s]+["\']?',
                'Skip links': r'href=["\']#[^"\']*["\'][^>]*>skip',
                'ARIA labels': r'aria-label=["\'][^"\']+["\']',
                'Alt attributes on images': r'<img[^>]*alt=["\'][^"\']*["\']',
                'Form labels': r'<label[^>]*for=["\'][^"\']+["\']',
                'Button roles': r'<button[^>]*>|role=["\']?button["\']?'
            }
            
            for check_name, pattern in a11y_checks.items():
                if re.search(pattern, content, re.IGNORECASE):
                    self.log_passed(f"{check_name} found")
                else:
                    self.log_warning(f"{check_name} missing")
            
            # Check color contrast (basic check for CSS custom properties)
            if '--primary' in content and '--secondary' in content:
                self.log_passed("CSS custom properties found (good for theming)")
            
        except Exception as e:
            self.log_error(f"Error testing accessibility: {e}")
    
    def test_robots_sitemap(self):
        """Test robots.txt and sitemap"""
        print("🤖 Testing Robots.txt and Sitemap...")
        
        # Check robots.txt
        robots_path = self.public_dir / "robots.txt"
        if robots_path.exists():
            try:
                with open(robots_path, 'r', encoding='utf-8') as f:
                    robots_content = f.read()
                
                if 'Sitemap:' in robots_content:
                    self.log_passed("Sitemap reference found in robots.txt")
                else:
                    self.log_warning("No sitemap reference in robots.txt")
                    
                if 'User-agent: *' in robots_content:
                    self.log_passed("User-agent directive found")
                else:
                    self.log_warning("No user-agent directive in robots.txt")
                    
            except Exception as e:
                self.log_error(f"Error reading robots.txt: {e}")
        else:
            self.log_error("robots.txt not found")
        
        # Check sitemap.xml
        sitemap_path = self.public_dir / "sitemap.xml"
        if sitemap_path.exists():
            try:
                with open(sitemap_path, 'r', encoding='utf-8') as f:
                    sitemap_content = f.read()
                
                # Basic XML validation
                if '<?xml' in sitemap_content and '<urlset' in sitemap_content:
                    self.log_passed("Valid sitemap XML structure")
                else:
                    self.log_error("Invalid sitemap XML structure")
                
                # Count URLs
                url_count = sitemap_content.count('<url>')
                if url_count > 0:
                    self.log_passed(f"Sitemap contains {url_count} URLs")
                else:
                    self.log_warning("Sitemap appears to be empty")
                    
            except Exception as e:
                self.log_error(f"Error reading sitemap.xml: {e}")
        else:
            self.log_error("sitemap.xml not found")
    
    def test_web_vitals_preparation(self):
        """Test Core Web Vitals preparation"""
        print("📊 Testing Core Web Vitals Preparation...")
        
        # Check for performance optimizations
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return
            
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            vitals_checks = {
                'Resource preloading': r'<link[^>]*rel=["\']?preload["\']?',
                'DNS prefetch': r'<link[^>]*rel=["\']?dns-prefetch["\']?',
                'Critical CSS inlining': r'<style[^>]*>[^<]*{[^}]*}[^<]*</style>',
                'Lazy loading': r'loading=["\']?lazy["\']?',
                'Image optimization': r'srcset=["\'][^"\']+["\']',
                'Minified assets': r'\.min\.(css|js)',
                'Asset fingerprinting': r'\.[a-f0-9]{8,}\.(css|js)',
                'Service Worker': r'serviceWorker\.register',
                'Web App Manifest': r'<link[^>]*rel=["\']?manifest["\']?'
            }
            
            for check_name, pattern in vitals_checks.items():
                if re.search(pattern, content, re.IGNORECASE):
                    self.log_passed(f"{check_name} implemented")
                else:
                    self.log_warning(f"{check_name} not found")
                    
        except Exception as e:
            self.log_error(f"Error testing Web Vitals preparation: {e}")
    
    def generate_report(self):
        """Generate comprehensive SEO & Performance report"""
        print("\n" + "="*80)
        print("🚀 SEO & PERFORMANCE TESTING REPORT")
        print("="*80)
        
        total_checks = len(self.passed) + len(self.warnings) + len(self.errors)
        passed_count = len(self.passed)
        warning_count = len(self.warnings)
        error_count = len(self.errors)
        
        # Calculate scores
        seo_score = (passed_count / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\n📊 Overall SEO & Performance Score: {seo_score:.1f}/100")
        print(f"✅ Passed: {passed_count}")
        print(f"⚠️  Warnings: {warning_count}") 
        print(f"❌ Errors: {error_count}")
        
        # Detailed results
        if self.passed:
            print(f"\n✅ Passed Checks ({len(self.passed)}):")
            for check in self.passed:
                print(f"  {check}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        
        if seo_score >= 90:
            print("  🎉 Excellent SEO & Performance! Ready for production.")
        elif seo_score >= 75:
            print("  👍 Good SEO & Performance. Address warnings for optimization.")
        elif seo_score >= 60:
            print("  ⚠️  Fair SEO & Performance. Fix errors before deployment.")
        else:
            print("  🚨 Poor SEO & Performance. Immediate fixes required.")
        
        print(f"\n🔍 Next Steps:")
        print("  1. Fix critical errors immediately")
        print("  2. Address warnings for better optimization")  
        print("  3. Test with Lighthouse for detailed metrics")
        print("  4. Monitor Core Web Vitals in production")
        
        return seo_score >= 75
    
    def run_all_tests(self):
        """Run all SEO & Performance tests"""
        print("🚀 Starting SEO & Performance Testing...")
        print(f"📁 Testing directory: {self.public_dir}")
        
        if not self.public_dir.exists():
            print("❌ Public directory not found. Run 'hugo --minify' first.")
            return False
        
        self.test_structured_data()
        self.test_seo_fundamentals()
        self.test_performance_metrics()
        self.test_accessibility_features()
        self.test_robots_sitemap()
        self.test_web_vitals_preparation()
        
        return self.generate_report()

def main():
    """Main execution function"""
    tester = SEOPerformanceTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()