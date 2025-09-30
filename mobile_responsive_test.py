#!/usr/bin/env python3
"""
Mobile Responsiveness and Core Web Vitals Testing
Phase 3.12: Final Testing & Validation
Tests mobile responsiveness and performance indicators
"""

import re
import sys
from pathlib import Path
import json

class MobileResponsiveTester:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.public_dir = self.root_dir / "public"
        self.results = {
            "viewport": {"score": 0, "details": []},
            "responsive_design": {"score": 0, "details": []},
            "touch_targets": {"score": 0, "details": []},
            "performance": {"score": 0, "details": []},
            "core_web_vitals": {"score": 0, "details": []}
        }
        self.issues = []
        self.recommendations = []
        
    def test_mobile_responsiveness(self):
        """Test mobile responsiveness across page types"""
        print("📱 Testing Mobile Responsiveness...")
        
        # Test key pages
        pages_to_test = {
            "Homepage": "index.html",
            "Blog Post": "posts/javascript-fundamentals/index.html",
            "Search Page": "search/index.html",
            "About Page": "about/index.html"
        }
        
        total_score = 0
        tested_pages = 0
        
        for page_type, page_path in pages_to_test.items():
            full_path = self.public_dir / page_path
            if full_path.exists():
                score = self._test_page_responsiveness(full_path, page_type)
                total_score += score
                tested_pages += 1
            else:
                self.issues.append(f"Page not found: {page_type} ({page_path})")
        
        return total_score / tested_pages if tested_pages > 0 else 0
    
    def _test_page_responsiveness(self, page_path, page_type):
        """Test responsiveness for a specific page"""
        try:
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Test various responsiveness aspects
            viewport_score = self._test_viewport_meta(content, page_type)
            css_score = self._test_responsive_css(content, page_type)
            images_score = self._test_responsive_images(content, page_type)
            typography_score = self._test_responsive_typography(content, page_type)
            
            # Calculate page responsiveness score
            page_score = (viewport_score + css_score + images_score + typography_score) / 4
            
            return page_score
            
        except Exception as e:
            self.issues.append(f"Error testing {page_type}: {e}")
            return 0
    
    def _test_viewport_meta(self, content, page_type):
        """Test viewport meta tag"""
        viewport_pattern = r'<meta[^>]*name=["\']viewport["\'][^>]*content=["\']([^"\']+)["\']'
        viewport_match = re.search(viewport_pattern, content, re.IGNORECASE)
        
        if not viewport_match:
            self.issues.append(f"{page_type}: Missing viewport meta tag")
            return 0
        
        viewport_content = viewport_match.group(1)
        
        # Check for proper viewport settings
        score = 0
        checks = {
            "width=device-width": 25,
            "initial-scale=1": 25,
            "shrink-to-fit=no": 25,
            "viewport-fit=cover": 25  # Optional but good for modern devices
        }
        
        for check, points in checks.items():
            if check in viewport_content:
                score += points
                self.results["viewport"]["details"].append(f"{page_type}: {check} ✅")
            else:
                if check != "viewport-fit=cover":  # This is optional
                    self.issues.append(f"{page_type}: Missing {check} in viewport")
        
        # Award full points if first 3 essential checks pass
        essential_checks = ["width=device-width", "initial-scale=1", "shrink-to-fit=no"]
        if all(check in viewport_content for check in essential_checks):
            score = 100
        
        return min(score, 100)
    
    def _test_responsive_css(self, content, page_type):
        """Test responsive CSS patterns"""
        score = 0
        
        # Look for media queries
        media_queries = re.findall(r'@media[^{]*\([^)]*\)', content, re.IGNORECASE)
        if media_queries:
            score += 30
            self.results["responsive_design"]["details"].append(f"{page_type}: Media queries found ✅")
        else:
            self.issues.append(f"{page_type}: No media queries found")
        
        # Look for flexible layouts
        flexible_patterns = [
            r'flex|grid|column',
            r'width.*%|max-width|min-width',
            r'responsive|mobile-first'
        ]
        
        for pattern in flexible_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                score += 20
                break
        
        # Look for CSS custom properties (good for responsive theming)
        if re.search(r'--[\w-]+:', content):
            score += 25
            self.results["responsive_design"]["details"].append(f"{page_type}: CSS custom properties ✅")
        
        # Look for modern CSS features
        modern_css = re.search(r'clamp|min|max|calc', content, re.IGNORECASE)
        if modern_css:
            score += 25
            self.results["responsive_design"]["details"].append(f"{page_type}: Modern CSS functions ✅")
        
        return min(score, 100)
    
    def _test_responsive_images(self, content, page_type):
        """Test responsive image implementation"""
        # Find all images
        images = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
        
        if not images:
            return 100  # No images is fine
        
        score = 0
        responsive_features = 0
        
        # Check for responsive image features
        for img in images:
            # Check for srcset
            if 'srcset=' in img.lower():
                responsive_features += 1
            
            # Check for sizes attribute
            if 'sizes=' in img.lower():
                responsive_features += 1
            
            # Check for loading attribute
            if 'loading=' in img.lower():
                responsive_features += 1
        
        if images:
            responsive_ratio = responsive_features / (len(images) * 3)  # 3 features per image max
            score = responsive_ratio * 100
        
        # Check for picture elements (advanced responsive images)
        picture_elements = len(re.findall(r'<picture[^>]*>', content, re.IGNORECASE))
        if picture_elements > 0:
            score = min(score + 20, 100)
            self.results["responsive_design"]["details"].append(f"{page_type}: Picture elements found ✅")
        
        if score >= 60:
            self.results["responsive_design"]["details"].append(f"{page_type}: Responsive images implemented ✅")
        else:
            self.issues.append(f"{page_type}: Images could be more responsive")
        
        return score
    
    def _test_responsive_typography(self, content, page_type):
        """Test responsive typography"""
        score = 0
        
        # Check for relative units
        relative_units = re.findall(r'font-size.*(?:rem|em|%|vw|vh)', content, re.IGNORECASE)
        if relative_units:
            score += 40
            self.results["responsive_design"]["details"].append(f"{page_type}: Relative font units ✅")
        
        # Check for responsive font scaling
        if re.search(r'clamp.*font|font.*clamp', content, re.IGNORECASE):
            score += 30
            self.results["responsive_design"]["details"].append(f"{page_type}: Fluid typography ✅")
        
        # Check for appropriate line-height
        if re.search(r'line-height.*1\.[3-7]', content):
            score += 30
            self.results["responsive_design"]["details"].append(f"{page_type}: Good line-height ✅")
        
        return min(score, 100)
    
    def test_touch_targets(self):
        """Test touch target sizes and spacing"""
        print("👆 Testing Touch Target Accessibility...")
        
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return 0
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            score = 0
            
            # Look for proper button sizing in CSS
            button_css = re.search(r'\.btn|button.*{[^}]*(?:min-height|padding)[^}]*}', content, re.IGNORECASE)
            if button_css:
                score += 30
                self.results["touch_targets"]["details"].append("Button sizing CSS found ✅")
            
            # Check for touch-friendly spacing
            spacing_css = re.search(r'margin|padding.*(?:1|2)(?:rem|em)', content, re.IGNORECASE)
            if spacing_css:
                score += 25
                self.results["touch_targets"]["details"].append("Touch-friendly spacing ✅")
            
            # Check for accessibility considerations
            accessible_buttons = re.search(r'min-height.*44|44.*px|2\.75.*rem', content, re.IGNORECASE)
            if accessible_buttons:
                score += 45
                self.results["touch_targets"]["details"].append("44px minimum touch targets ✅")
            
            return score
            
        except Exception as e:
            self.issues.append(f"Error testing touch targets: {e}")
            return 0
    
    def test_core_web_vitals_prep(self):
        """Test Core Web Vitals preparation"""
        print("📊 Testing Core Web Vitals Preparation...")
        
        index_path = self.public_dir / "index.html"
        if not index_path.exists():
            return 0
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            score = 0
            
            # Largest Contentful Paint (LCP) optimizations
            lcp_optimizations = [
                ("Critical CSS inlining", r'<style[^>]*>[^<]*{'),
                ("Resource preloading", r'rel=["\']preload["\']'),
                ("Image optimization", r'loading=["\']lazy["\']|srcset='),
                ("Font optimization", r'font-display|preload.*font')
            ]
            
            for opt_name, pattern in lcp_optimizations:
                if re.search(pattern, content, re.IGNORECASE):
                    score += 15
                    self.results["core_web_vitals"]["details"].append(f"LCP: {opt_name} ✅")
            
            # First Input Delay (FID) optimizations
            fid_optimizations = [
                ("JavaScript optimization", r'async|defer'),
                ("Service Worker", r'serviceWorker'),
                ("Code splitting", r'dynamic.*import|lazy.*load')
            ]
            
            for opt_name, pattern in fid_optimizations:
                if re.search(pattern, content, re.IGNORECASE):
                    score += 10
                    self.results["core_web_vitals"]["details"].append(f"FID: {opt_name} ✅")
            
            # Cumulative Layout Shift (CLS) optimizations
            cls_optimizations = [
                ("Image dimensions", r'width=.*height=|aspect-ratio'),
                ("Font loading", r'font-display'),
                ("Reserved space", r'min-height|placeholder')
            ]
            
            for opt_name, pattern in cls_optimizations:
                if re.search(pattern, content, re.IGNORECASE):
                    score += 10
                    self.results["core_web_vitals"]["details"].append(f"CLS: {opt_name} ✅")
            
            return min(score, 100)
            
        except Exception as e:
            self.issues.append(f"Error testing Core Web Vitals: {e}")
            return 0
    
    def test_mobile_performance(self):
        """Test mobile-specific performance indicators"""
        print("⚡ Testing Mobile Performance...")
        
        score = 0
        
        # Check file sizes
        index_path = self.public_dir / "index.html"
        if index_path.exists():
            index_size = index_path.stat().st_size / 1024  # KB
            
            if index_size < 50:  # Less than 50KB is excellent for mobile
                score += 30
                self.results["performance"]["details"].append(f"Homepage size optimal: {index_size:.1f}KB ✅")
            elif index_size < 100:
                score += 20
                self.results["performance"]["details"].append(f"Homepage size good: {index_size:.1f}KB ✅")
            else:
                self.issues.append(f"Homepage size large: {index_size:.1f}KB")
        
        # Check for minified assets
        css_files = list(self.public_dir.rglob("*.css"))
        js_files = list(self.public_dir.rglob("*.js"))
        
        minified_assets = 0
        total_assets = len(css_files) + len(js_files)
        
        for asset_file in css_files + js_files:
            try:
                with open(asset_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple minification check
                if len(content.split('\n')) < 10 and len(content) > 500:
                    minified_assets += 1
            except Exception:
                continue
        
        if total_assets > 0:
            minification_ratio = minified_assets / total_assets
            score += minification_ratio * 30
            
            if minification_ratio > 0.8:
                self.results["performance"]["details"].append("Assets properly minified ✅")
        
        # Check for compression indicators
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for gzip/compression preparation
            if 'integrity=' in content:  # Subresource integrity suggests build optimization
                score += 20
                self.results["performance"]["details"].append("Asset integrity hashes ✅")
            
            # Check for performance optimizations
            if 'dns-prefetch' in content:
                score += 10
                self.results["performance"]["details"].append("DNS prefetch optimization ✅")
            
            if 'preconnect' in content:
                score += 10
                self.results["performance"]["details"].append("Preconnect optimization ✅")
        
        return min(score, 100)
    
    def generate_mobile_report(self):
        """Generate comprehensive mobile responsiveness report"""
        print("\n" + "="*80)
        print("📱 MOBILE RESPONSIVENESS & CORE WEB VITALS REPORT")
        print("="*80)
        
        # Run all tests
        responsive_score = self.test_mobile_responsiveness()
        touch_score = self.test_touch_targets()
        vitals_score = self.test_core_web_vitals_prep()
        performance_score = self.test_mobile_performance()
        
        # Calculate overall mobile score
        overall_score = (responsive_score + touch_score + vitals_score + performance_score) / 4
        
        # Update results
        self.results["responsive_design"]["score"] = responsive_score
        self.results["touch_targets"]["score"] = touch_score
        self.results["core_web_vitals"]["score"] = vitals_score
        self.results["performance"]["score"] = performance_score
        
        print(f"\n📊 Mobile Performance Scores:")
        print(f"  📱 Responsive Design: {responsive_score:.0f}/100")
        print(f"  👆 Touch Targets: {touch_score:.0f}/100")
        print(f"  📊 Core Web Vitals Prep: {vitals_score:.0f}/100")
        print(f"  ⚡ Mobile Performance: {performance_score:.0f}/100")
        print(f"  🎯 Overall Mobile Score: {overall_score:.0f}/100")
        
        # Grade the mobile experience
        if overall_score >= 90:
            grade = "🟢 EXCELLENT"
            status = "Outstanding mobile experience!"
        elif overall_score >= 75:
            grade = "🟡 GOOD"
            status = "Good mobile experience with minor improvements possible"
        elif overall_score >= 60:
            grade = "🟠 FAIR"
            status = "Acceptable mobile experience, improvements recommended"
        else:
            grade = "🔴 POOR"
            status = "Mobile experience needs significant improvement"
        
        print(f"\n🏆 Mobile Grade: {grade}")
        print(f"📋 Status: {status}")
        
        # Show successful optimizations
        print(f"\n✅ Mobile Optimizations Found:")
        for category, data in self.results.items():
            if data["details"]:
                print(f"  {category.replace('_', ' ').title()}:")
                for detail in data["details"]:
                    print(f"    ✅ {detail}")
        
        # Show issues
        if self.issues:
            print(f"\n⚠️  Mobile Issues to Address ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  ⚠️ {issue}")
        
        # Recommendations
        print(f"\n💡 Mobile Optimization Recommendations:")
        
        if overall_score >= 90:
            print("  🎉 Excellent mobile optimization! Your site provides a great mobile experience.")
            print("  📊 Monitor Core Web Vitals in production for ongoing optimization.")
        elif overall_score >= 75:
            print("  👍 Good mobile foundation. Consider these improvements:")
            print("  📱 Test on various devices and screen sizes.")
            print("  ⚡ Monitor loading performance on 3G connections.")
        else:
            print("  🚨 Mobile experience improvements needed:")
            print("  📏 Ensure proper viewport meta tag configuration.")
            print("  👆 Verify touch targets are at least 44px in size.")
            print("  📊 Optimize images and assets for mobile bandwidth.")
            print("  🎨 Test responsive design across different breakpoints.")
        
        # Core Web Vitals guidance
        print(f"\n📊 Core Web Vitals Guidance:")
        print("  • LCP (Largest Contentful Paint): < 2.5s")
        print("  • FID (First Input Delay): < 100ms")
        print("  • CLS (Cumulative Layout Shift): < 0.1")
        print("  • Use tools like Lighthouse and PageSpeed Insights for production testing")
        
        return overall_score >= 75

def main():
    """Main execution function"""
    print("🚀 Starting Mobile Responsiveness & Core Web Vitals Testing...")
    
    tester = MobileResponsiveTester()
    success = tester.generate_mobile_report()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()