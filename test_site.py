#!/usr/bin/env python3
"""
Comprehensive Site Testing Script
Phase 3.9: Content Validation & Testing
"""

import json
import re
import subprocess
import sys
import os
from pathlib import Path
from urllib.parse import urljoin, urlparse
import time

class SiteTester:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.public_dir = self.root_dir / "public"
        self.results = {"passed": [], "failed": [], "warnings": []}
        
    def test_hugo_build(self):
        """Test if Hugo builds without errors"""
        print("🔨 Testing Hugo build...")
        try:
            result = subprocess.run(
                ["hugo", "--minify"], 
                cwd=self.root_dir, 
                capture_output=True, 
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.results["passed"].append("✅ Hugo build successful")
                return True
            else:
                self.results["failed"].append(f"❌ Hugo build failed: {result.stderr}")
                return False
        except Exception as e:
            self.results["failed"].append(f"❌ Hugo build error: {e}")
            return False
    
    def test_essential_pages(self):
        """Test that essential pages exist and have content"""
        print("📄 Testing essential pages...")
        
        essential_pages = {
            "public/index.html": "Homepage",
            "public/search/index.html": "Search page", 
            "public/about/index.html": "About page",
            "public/posts/index.html": "Posts listing",
            "public/sitemap.xml": "Sitemap",
            "public/robots.txt": "Robots.txt",
            "public/index.json": "Search index"
        }
        
        all_passed = True
        for file_path, description in essential_pages.items():
            full_path = self.root_dir / file_path
            if full_path.exists() and full_path.stat().st_size > 0:
                self.results["passed"].append(f"✅ {description} exists and has content")
            else:
                self.results["failed"].append(f"❌ {description} missing or empty")
                all_passed = False
        
        return all_passed
    
    def test_search_functionality(self):
        """Test search index and page"""
        print("🔍 Testing search functionality...")
        
        search_index_path = self.public_dir / "index.json"
        search_page_path = self.public_dir / "search" / "index.html"
        
        # Test search index
        try:
            with open(search_index_path, 'r') as f:
                search_data = json.load(f)
            
            if isinstance(search_data, list) and len(search_data) > 0:
                self.results["passed"].append(f"✅ Search index valid ({len(search_data)} entries)")
                
                # Test index structure
                required_keys = ["title", "content", "permalink", "summary"]
                first_entry = search_data[0]
                missing_keys = [key for key in required_keys if key not in first_entry]
                
                if not missing_keys:
                    self.results["passed"].append("✅ Search index structure valid")
                else:
                    self.results["failed"].append(f"❌ Search index missing keys: {missing_keys}")
            else:
                self.results["failed"].append("❌ Search index invalid or empty")
                
        except Exception as e:
            self.results["failed"].append(f"❌ Search index error: {e}")
        
        # Test search page elements
        try:
            with open(search_page_path, 'r') as f:
                search_html = f.read()
            
            if 'id="searchInput"' in search_html or 'id=searchInput' in search_html:
                self.results["passed"].append("✅ Search input element found")
            else:
                self.results["failed"].append("❌ Search input element missing")
                
            if 'id="searchResults"' in search_html or 'id=searchResults' in search_html:
                self.results["passed"].append("✅ Search results element found") 
            else:
                self.results["failed"].append("❌ Search results element missing")
                
        except Exception as e:
            self.results["failed"].append(f"❌ Search page error: {e}")
    
    def test_content_validation(self):
        """Test content quality and structure"""
        print("📝 Testing content validation...")
        
        # Check for posts
        posts_dir = self.public_dir / "posts"
        if posts_dir.exists():
            post_dirs = [d for d in posts_dir.iterdir() if d.is_dir()]
            if len(post_dirs) >= 3:
                self.results["passed"].append(f"✅ Sufficient content ({len(post_dirs)} posts)")
            else:
                self.results["warnings"].append(f"⚠️ Limited content ({len(post_dirs)} posts)")
        
        # Check RSS feed
        rss_path = self.public_dir / "index.xml"
        if rss_path.exists():
            with open(rss_path, 'r') as f:
                rss_content = f.read()
            if '<item>' in rss_content:
                self.results["passed"].append("✅ RSS feed has content")
            else:
                self.results["warnings"].append("⚠️ RSS feed appears empty")
    
    def test_seo_elements(self):
        """Test SEO and meta elements"""
        print("🔍 Testing SEO elements...")
        
        index_path = self.public_dir / "index.html"
        try:
            with open(index_path, 'r') as f:
                content = f.read()
            
            seo_tests = {
                "Title tag": r'<title[^>]*>[^<]+</title>',
                "Meta description": r'<meta[^>]*name=["\']description["\'][^>]*content=["\'][^"\']+["\']',
                "Meta viewport": r'<meta[^>]*name=["\']viewport["\']',
                "Canonical URL": r'<link[^>]*rel=["\']canonical["\']',
                "Open Graph title": r'<meta[^>]*property=["\']og:title["\']',
                "Structured data": r'<script[^>]*type=["\']application/ld\+json["\']'
            }
            
            for test_name, pattern in seo_tests.items():
                if re.search(pattern, content, re.IGNORECASE):
                    self.results["passed"].append(f"✅ {test_name} found")
                else:
                    self.results["warnings"].append(f"⚠️ {test_name} missing")
                    
        except Exception as e:
            self.results["failed"].append(f"❌ SEO test error: {e}")
    
    def test_performance_basics(self):
        """Test basic performance indicators"""
        print("⚡ Testing performance basics...")
        
        # Check file sizes
        index_path = self.public_dir / "index.html"
        if index_path.exists():
            size_kb = index_path.stat().st_size / 1024
            if size_kb < 100:  # Under 100KB is good
                self.results["passed"].append(f"✅ Homepage size optimal ({size_kb:.1f}KB)")
            else:
                self.results["warnings"].append(f"⚠️ Homepage large ({size_kb:.1f}KB)")
        
        # Check for minification
        try:
            with open(index_path, 'r') as f:
                content = f.read()
            
            if len(content.split('\n')) < 10:  # Very few lines = minified
                self.results["passed"].append("✅ HTML appears minified")
            else:
                self.results["warnings"].append("⚠️ HTML may not be minified")
                
        except Exception as e:
            self.results["warnings"].append(f"⚠️ Minification check failed: {e}")
    
    def test_accessibility_basics(self):
        """Test basic accessibility features"""
        print("♿ Testing accessibility basics...")
        
        index_path = self.public_dir / "index.html"
        try:
            with open(index_path, 'r') as f:
                content = f.read()
            
            # Check for accessibility features
            a11y_tests = {
                "Alt attributes": r'<img[^>]*alt=["\'][^"\']*["\']',
                "ARIA labels": r'aria-label=["\'][^"\']+["\']',
                "Skip links": r'href=["\']#[^"\']*["\'][^>]*>skip',
                "Language attribute": r'<html[^>]*lang=["\'][^"\']+["\']'
            }
            
            for test_name, pattern in a11y_tests.items():
                if re.search(pattern, content, re.IGNORECASE):
                    self.results["passed"].append(f"✅ {test_name} found")
                else:
                    self.results["warnings"].append(f"⚠️ {test_name} missing")
                    
        except Exception as e:
            self.results["warnings"].append(f"⚠️ Accessibility test error: {e}")
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🧪 Starting comprehensive site testing...")
        print("="*50)
        
        # Run tests in order
        build_success = self.test_hugo_build()
        if not build_success:
            print("❌ Build failed - stopping tests")
            return False
        
        self.test_essential_pages()
        self.test_search_functionality()
        self.test_content_validation()
        self.test_seo_elements()
        self.test_performance_basics()
        self.test_accessibility_basics()
        
        # Generate report
        self.generate_report()
        
        return len(self.results["failed"]) == 0
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*50)
        print("🧪 COMPREHENSIVE SITE TESTING REPORT")
        print("="*50)
        
        passed = len(self.results["passed"])
        failed = len(self.results["failed"])
        warnings = len(self.results["warnings"])
        total = passed + failed + warnings
        
        print(f"\n📊 Summary:")
        print(f"  ✅ Passed: {passed}")
        print(f"  ❌ Failed: {failed}")
        print(f"  ⚠️  Warnings: {warnings}")
        print(f"  📈 Success Rate: {(passed/total*100):.1f}%")
        
        if self.results["passed"]:
            print(f"\n✅ Passed Tests ({passed}):")
            for test in self.results["passed"]:
                print(f"  {test}")
        
        if self.results["warnings"]:
            print(f"\n⚠️  Warnings ({warnings}):")
            for warning in self.results["warnings"]:
                print(f"  {warning}")
        
        if self.results["failed"]:
            print(f"\n❌ Failed Tests ({failed}):")
            for failure in self.results["failed"]:
                print(f"  {failure}")
        
        print(f"\n{'='*50}")
        if failed == 0:
            if warnings == 0:
                print("🎉 ALL TESTS PASSED - Site is production ready!")
            else:
                print("🟡 TESTS PASSED WITH WARNINGS - Consider addressing warnings")
        else:
            print("🔴 SOME TESTS FAILED - Fix failed tests before deployment")

def main():
    """Main test execution"""
    tester = SiteTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()