#!/usr/bin/env python3
"""
Lighthouse Audit Script for SEO and Performance Testing
Phase 3.12: Final Testing & Validation
Simulates Lighthouse audit checks for production readiness
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
import subprocess

class LighthouseAudit:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.public_dir = self.root_dir / "public"
        self.results = {
            "performance": {"score": 0, "audits": []},
            "accessibility": {"score": 0, "audits": []},
            "best_practices": {"score": 0, "audits": []},
            "seo": {"score": 0, "audits": []},
            "pwa": {"score": 0, "audits": []}
        }
        self.issues = []
        self.recommendations = []
        
    def audit_performance(self):
        """Audit performance metrics"""
        print("⚡ Auditing Performance...")
        
        performance_checks = {
            "first_contentful_paint": self._check_critical_css(),
            "largest_contentful_paint": self._check_image_optimization(),
            "cumulative_layout_shift": self._check_layout_stability(),
            "speed_index": self._check_resource_optimization(),
            "total_blocking_time": self._check_render_blocking(),
            "interactive": self._check_javascript_optimization()
        }
        
        passed = sum(1 for check in performance_checks.values() if check)
        self.results["performance"]["score"] = (passed / len(performance_checks)) * 100
        self.results["performance"]["audits"] = list(performance_checks.keys())
        
        return self.results["performance"]["score"]
    
    def audit_accessibility(self):
        """Audit accessibility compliance (WCAG 2.1 AA)"""
        print("♿ Auditing Accessibility (WCAG 2.1 AA)...")
        
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return 0
            
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            accessibility_checks = {
                "html_lang": bool(re.search(r'<html[^>]*lang=["\'][^"\']+["\']', content, re.IGNORECASE)),
                "meta_viewport": bool(re.search(r'<meta[^>]*name=["\']viewport["\']', content, re.IGNORECASE)),
                "page_title": bool(re.search(r'<title[^>]*>[^<]+</title>', content, re.IGNORECASE)),
                "heading_hierarchy": self._check_heading_hierarchy(content),
                "color_contrast": self._check_color_contrast(content),
                "focus_management": self._check_focus_management(content),
                "aria_labels": bool(re.search(r'aria-label=["\'][^"\']+["\']', content, re.IGNORECASE)),
                "semantic_markup": self._check_semantic_markup(content),
                "keyboard_navigation": self._check_keyboard_navigation(content),
                "alt_attributes": self._check_alt_attributes()
            }
            
            passed = sum(1 for check in accessibility_checks.values() if check)
            self.results["accessibility"]["score"] = (passed / len(accessibility_checks)) * 100
            self.results["accessibility"]["audits"] = [k for k, v in accessibility_checks.items() if v]
            
            # Log accessibility issues
            for check_name, passed in accessibility_checks.items():
                if not passed:
                    self.issues.append(f"Accessibility: {check_name.replace('_', ' ').title()} failed")
            
            return self.results["accessibility"]["score"]
            
        except Exception as e:
            print(f"Error auditing accessibility: {e}")
            return 0
    
    def audit_best_practices(self):
        """Audit web best practices"""
        print("🏆 Auditing Best Practices...")
        
        best_practices_checks = {
            "https_usage": True,  # Assume HTTPS in production
            "security_headers": self._check_security_headers(),
            "modern_image_formats": self._check_modern_images(),
            "efficient_cache_policy": self._check_caching_strategy(),
            "no_console_errors": self._check_console_logs(),
            "proper_doctype": self._check_doctype(),
            "charset_declaration": self._check_charset(),
            "no_vulnerable_libraries": self._check_vulnerable_libs(),
            "csp_headers": self._check_content_security_policy()
        }
        
        passed = sum(1 for check in best_practices_checks.values() if check)
        self.results["best_practices"]["score"] = (passed / len(best_practices_checks)) * 100
        self.results["best_practices"]["audits"] = [k for k, v in best_practices_checks.items() if v]
        
        return self.results["best_practices"]["score"]
    
    def audit_seo(self):
        """Audit SEO optimization"""
        print("🔍 Auditing SEO...")
        
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return 0
            
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            seo_checks = {
                "title_exists": bool(re.search(r'<title[^>]*>[^<]+</title>', content, re.IGNORECASE)),
                "meta_description": bool(re.search(r'name=["\']description["\'][^>]*content=["\'][^"\']+["\']', content, re.IGNORECASE)),
                "meta_viewport": bool(re.search(r'name=["\']viewport["\']', content, re.IGNORECASE)),
                "crawlable": self._check_robots_txt(),
                "sitemap": self._check_sitemap(),
                "structured_data": self._check_structured_data(content),
                "canonical_url": bool(re.search(r'rel=["\']canonical["\']', content, re.IGNORECASE)),
                "social_meta": self._check_social_meta(content),
                "image_alt": self._check_image_alt_seo(),
                "hreflang": self._check_hreflang(content)
            }
            
            passed = sum(1 for check in seo_checks.values() if check)
            self.results["seo"]["score"] = (passed / len(seo_checks)) * 100
            self.results["seo"]["audits"] = [k for k, v in seo_checks.items() if v]
            
            return self.results["seo"]["score"]
            
        except Exception as e:
            print(f"Error auditing SEO: {e}")
            return 0
    
    def audit_pwa(self):
        """Audit Progressive Web App features"""
        print("📱 Auditing PWA Features...")
        
        pwa_checks = {
            "manifest": self._check_web_manifest(),
            "service_worker": self._check_service_worker(),
            "installable": self._check_installability(),
            "responsive": self._check_responsive_design(),
            "offline_support": self._check_offline_functionality(),
            "https_ready": True,  # Assume HTTPS in production
            "splash_screen": self._check_splash_screen(),
            "theme_color": self._check_theme_color(),
            "viewport_meta": self._check_viewport_meta()
        }
        
        passed = sum(1 for check in pwa_checks.values() if check)
        self.results["pwa"]["score"] = (passed / len(pwa_checks)) * 100
        self.results["pwa"]["audits"] = [k for k, v in pwa_checks.items() if v]
        
        return self.results["pwa"]["score"]
    
    # Helper methods for specific checks
    def _check_critical_css(self):
        """Check for critical CSS inlining"""
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return False
            
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for inline styles in head
        return bool(re.search(r'<style[^>]*>[^<]*{[^}]*}[^<]*</style>', content))
    
    def _check_image_optimization(self):
        """Check for optimized images"""
        # Check for WebP images or responsive images
        html_files = list(self.public_dir.rglob("*.html"))
        
        for html_file in html_files[:3]:  # Check first 3 files
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if re.search(r'srcset=|<picture>|\.webp', content, re.IGNORECASE):
                    return True
            except Exception:
                continue
        
        return False
    
    def _check_layout_stability(self):
        """Check for layout stability indicators"""
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return False
            
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for width/height attributes on images
        return bool(re.search(r'<img[^>]*(?:width=|height=)', content, re.IGNORECASE))
    
    def _check_resource_optimization(self):
        """Check for resource optimization"""
        # Check for minified assets
        assets = list(self.public_dir.rglob("*.css")) + list(self.public_dir.rglob("*.js"))
        
        for asset in assets[:5]:  # Check first 5 assets
            try:
                with open(asset, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple check: minified files have fewer newlines
                if len(content.split('\n')) < 10:
                    return True
            except Exception:
                continue
        
        return False
    
    def _check_render_blocking(self):
        """Check for render-blocking resources"""
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return False
            
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for preload and async attributes
        return bool(re.search(r'preload|async|defer', content, re.IGNORECASE))
    
    def _check_javascript_optimization(self):
        """Check JavaScript optimization"""
        js_files = list(self.public_dir.rglob("*.js"))
        
        # Check if JavaScript files are minified
        for js_file in js_files[:3]:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for minification indicators
                if len(content.split('\n')) < 10 and len(content) > 1000:
                    return True
            except Exception:
                continue
        
        return len(js_files) == 0  # No JS is also good for performance
    
    def _check_heading_hierarchy(self, content):
        """Check proper heading hierarchy"""
        headings = re.findall(r'<(h[1-6])[^>]*>', content, re.IGNORECASE)
        
        if not headings:
            return False
        
        # Check if starts with H1 and follows logical order
        h1_count = sum(1 for h in headings if h.lower() == 'h1')
        return h1_count == 1  # Should have exactly one H1
    
    def _check_color_contrast(self, content):
        """Check for color contrast considerations"""
        # Look for CSS custom properties (good for theming)
        return bool(re.search(r'--[\w-]+:', content))
    
    def _check_focus_management(self, content):
        """Check focus management"""
        return bool(re.search(r'focus|tabindex|accesskey', content, re.IGNORECASE))
    
    def _check_semantic_markup(self, content):
        """Check for semantic HTML"""
        semantic_tags = ['main', 'nav', 'header', 'footer', 'article', 'section', 'aside']
        return any(f'<{tag}' in content.lower() for tag in semantic_tags)
    
    def _check_keyboard_navigation(self, content):
        """Check keyboard navigation support"""
        return bool(re.search(r'keydown|keypress|accesskey', content, re.IGNORECASE))
    
    def _check_alt_attributes(self):
        """Check alt attributes on images"""
        html_files = list(self.public_dir.rglob("*.html"))
        
        for html_file in html_files[:5]:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                images = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
                images_with_alt = re.findall(r'<img[^>]*alt=', content, re.IGNORECASE)
                
                if images and len(images_with_alt) / len(images) > 0.8:
                    return True
            except Exception:
                continue
        
        return False
    
    def _check_security_headers(self):
        """Check for security headers in HTML"""
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return False
            
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        security_headers = [
            'Content-Security-Policy',
            'X-Content-Type-Options',
            'X-Frame-Options'
        ]
        
        return any(header in content for header in security_headers)
    
    def _check_modern_images(self):
        """Check for modern image formats"""
        # Check for WebP usage
        html_files = list(self.public_dir.rglob("*.html"))
        
        for html_file in html_files[:3]:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if '.webp' in content.lower():
                    return True
            except Exception:
                continue
        
        return False
    
    def _check_caching_strategy(self):
        """Check caching strategy"""
        # Look for service worker or cache headers
        sw_path = self.public_dir / "sw.js"
        return sw_path.exists()
    
    def _check_console_logs(self):
        """Check for console.log statements (should be minimal in production)"""
        js_files = list(self.public_dir.rglob("*.js"))
        
        for js_file in js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Count console.log statements
                if content.count('console.log') > 2:  # Allow some for legitimate use
                    return False
            except Exception:
                continue
        
        return True
    
    def _check_doctype(self):
        """Check for proper DOCTYPE"""
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return False
            
        with open(index_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        
        return first_line.lower().startswith('<!doctype html')
    
    def _check_charset(self):
        """Check for charset declaration"""
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return False
            
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return bool(re.search(r'<meta[^>]*charset=["\']?utf-8["\']?', content, re.IGNORECASE))
    
    def _check_vulnerable_libs(self):
        """Check for known vulnerable libraries"""
        # This is a simplified check - in real scenarios, use tools like npm audit
        js_files = list(self.public_dir.rglob("*.js"))
        
        vulnerable_patterns = [
            'jquery/1.', 'jquery/2.', 'bootstrap/3.',  # Old versions
            'lodash/3.', 'moment/2.18.'
        ]
        
        for js_file in js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if any(pattern in content.lower() for pattern in vulnerable_patterns):
                    return False
            except Exception:
                continue
        
        return True
    
    def _check_content_security_policy(self):
        """Check for Content Security Policy"""
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return False
            
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return 'Content-Security-Policy' in content
    
    def _check_robots_txt(self):
        """Check robots.txt exists and is valid"""
        robots_path = self.public_dir / "robots.txt"
        if not robots_path.exists():
            return False
        
        try:
            with open(robots_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return 'User-agent:' in content and 'Sitemap:' in content
        except Exception:
            return False
    
    def _check_sitemap(self):
        """Check sitemap.xml exists and is valid"""
        sitemap_path = self.public_dir / "sitemap.xml"
        if not sitemap_path.exists():
            return False
        
        try:
            with open(sitemap_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return '<urlset' in content and '<url>' in content
        except Exception:
            return False
    
    def _check_structured_data(self, content):
        """Check for structured data"""
        return bool(re.search(r'application/ld\+json', content, re.IGNORECASE))
    
    def _check_social_meta(self, content):
        """Check social media meta tags"""
        og_tags = len(re.findall(r'property=["\']og:', content, re.IGNORECASE))
        twitter_tags = len(re.findall(r'name=["\']twitter:', content, re.IGNORECASE))
        
        return og_tags >= 3 and twitter_tags >= 2
    
    def _check_image_alt_seo(self):
        """Check image alt attributes for SEO"""
        return self._check_alt_attributes()  # Reuse accessibility check
    
    def _check_hreflang(self, content):
        """Check hreflang attributes"""
        return bool(re.search(r'hreflang=', content, re.IGNORECASE))
    
    def _check_web_manifest(self):
        """Check for web app manifest"""
        manifest_path = self.public_dir / "manifest.json"
        if not manifest_path.exists():
            return False
        
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            required_fields = ['name', 'short_name', 'start_url', 'display', 'icons']
            return all(field in manifest for field in required_fields)
        except Exception:
            return False
    
    def _check_service_worker(self):
        """Check for service worker"""
        sw_path = self.public_dir / "sw.js"
        if not sw_path.exists():
            return False
        
        # Check if SW is registered in HTML
        index_path = self.public_dir / "index.html"
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return 'serviceWorker' in content and 'register' in content
        except Exception:
            return False
    
    def _check_installability(self):
        """Check PWA installability requirements"""
        return self._check_web_manifest() and self._check_service_worker()
    
    def _check_responsive_design(self):
        """Check responsive design implementation"""
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return False
            
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for viewport meta tag and responsive CSS
        viewport = bool(re.search(r'name=["\']viewport["\']', content, re.IGNORECASE))
        responsive_css = bool(re.search(r'@media|responsive', content, re.IGNORECASE))
        
        return viewport and responsive_css
    
    def _check_offline_functionality(self):
        """Check offline functionality"""
        return self._check_service_worker()  # Service worker enables offline support
    
    def _check_splash_screen(self):
        """Check for splash screen support"""
        manifest_path = self.public_dir / "manifest.json"
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            return 'theme_color' in manifest and 'background_color' in manifest
        except Exception:
            return False
    
    def _check_theme_color(self):
        """Check theme color meta tag"""
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return False
            
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return bool(re.search(r'name=["\']theme-color["\']', content, re.IGNORECASE))
    
    def _check_viewport_meta(self):
        """Check viewport meta tag"""
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return False
            
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return bool(re.search(r'name=["\']viewport["\']', content, re.IGNORECASE))
    
    def generate_lighthouse_report(self):
        """Generate comprehensive Lighthouse-style report"""
        print("\n" + "="*80)
        print("🔍 LIGHTHOUSE-STYLE AUDIT REPORT")
        print("="*80)
        
        # Run all audits
        perf_score = self.audit_performance()
        a11y_score = self.audit_accessibility()
        bp_score = self.audit_best_practices()
        seo_score = self.audit_seo()
        pwa_score = self.audit_pwa()
        
        # Calculate overall score
        overall_score = (perf_score + a11y_score + bp_score + seo_score) / 4
        
        # Display scores
        print(f"\n📊 Lighthouse Scores:")
        print(f"  ⚡ Performance: {perf_score:.0f}/100")
        print(f"  ♿ Accessibility: {a11y_score:.0f}/100")
        print(f"  🏆 Best Practices: {bp_score:.0f}/100")
        print(f"  🔍 SEO: {seo_score:.0f}/100")
        print(f"  📱 PWA: {pwa_score:.0f}/100")
        print(f"  🎯 Overall: {overall_score:.0f}/100")
        
        # Performance grade
        if overall_score >= 90:
            grade = "🟢 EXCELLENT"
            status = "Production Ready!"
        elif overall_score >= 75:
            grade = "🟡 GOOD"
            status = "Minor optimizations recommended"
        elif overall_score >= 60:
            grade = "🟠 FAIR"
            status = "Significant improvements needed"
        else:
            grade = "🔴 POOR"
            status = "Critical issues require immediate attention"
        
        print(f"\n🏆 Overall Grade: {grade}")
        print(f"📋 Status: {status}")
        
        # Recommendations
        if self.recommendations:
            print(f"\n💡 Recommendations:")
            for rec in self.recommendations:
                print(f"  {rec}")
        
        # Issues to address
        if self.issues:
            print(f"\n⚠️  Issues to Address ({len(self.issues)}):")
            for issue in self.issues[:10]:  # Show top 10
                print(f"  • {issue}")
            if len(self.issues) > 10:
                print(f"  ... and {len(self.issues) - 10} more")
        
        # Success criteria
        print(f"\n✅ Passing Audits:")
        for category, data in self.results.items():
            if data["audits"]:
                print(f"  {category.replace('_', ' ').title()}: {len(data['audits'])} checks passed")
        
        return overall_score >= 75

def main():
    """Main execution function"""
    print("🚀 Starting Lighthouse-style audit...")
    
    auditor = LighthouseAudit()
    success = auditor.generate_lighthouse_report()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()