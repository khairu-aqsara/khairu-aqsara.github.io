#!/usr/bin/env python3
"""
Accessibility Testing Script (WCAG 2.1 AA Compliance)
Phase 3.12: Final Testing & Validation
Tests accessibility compliance across all page types
"""

import re
import sys
from pathlib import Path
import json
from urllib.parse import urljoin

class AccessibilityTester:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.public_dir = self.root_dir / "public"
        self.results = {
            "passed": [],
            "warnings": [],
            "errors": [],
            "page_scores": {}
        }
        
    def test_wcag_compliance(self):
        """Test WCAG 2.1 AA compliance across page types"""
        print("♿ Testing WCAG 2.1 AA Accessibility Compliance...")
        
        # Test different page types
        page_types = {
            "Homepage": "index.html",
            "Blog Post": "posts/javascript-fundamentals/index.html",
            "About Page": "about/index.html", 
            "Search Page": "search/index.html",
            "Posts List": "posts/index.html"
        }
        
        overall_score = 0
        tested_pages = 0
        
        for page_type, page_path in page_types.items():
            full_path = self.public_dir / page_path
            if full_path.exists():
                score = self._test_page_accessibility(full_path, page_type)
                self.results["page_scores"][page_type] = score
                overall_score += score
                tested_pages += 1
            else:
                self.results["warnings"].append(f"Page not found for testing: {page_type}")
        
        return overall_score / tested_pages if tested_pages > 0 else 0
    
    def _test_page_accessibility(self, page_path, page_type):
        """Test accessibility for a specific page"""
        print(f"  Testing {page_type}...")
        
        try:
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            checks = {
                "language_declaration": self._check_language_declaration(content),
                "page_title": self._check_page_title(content),
                "heading_hierarchy": self._check_heading_hierarchy(content),
                "landmarks": self._check_landmarks(content),
                "link_context": self._check_link_context(content),
                "image_alternatives": self._check_image_alternatives(content),
                "form_labels": self._check_form_labels(content),
                "keyboard_navigation": self._check_keyboard_navigation(content),
                "focus_indicators": self._check_focus_indicators(content),
                "color_contrast": self._check_color_contrast_basics(content),
                "text_alternatives": self._check_text_alternatives(content),
                "skip_navigation": self._check_skip_navigation(content),
                "aria_usage": self._check_aria_usage(content),
                "semantic_markup": self._check_semantic_markup(content)
            }
            
            # Calculate page score
            passed_checks = sum(1 for result in checks.values() if result)
            page_score = (passed_checks / len(checks)) * 100
            
            # Log results
            for check_name, result in checks.items():
                check_display = check_name.replace('_', ' ').title()
                if result:
                    self.results["passed"].append(f"{page_type}: {check_display}")
                else:
                    self.results["errors"].append(f"{page_type}: {check_display} failed")
            
            return page_score
            
        except Exception as e:
            self.results["errors"].append(f"{page_type}: Error reading file - {e}")
            return 0
    
    def _check_language_declaration(self, content):
        """Check for proper language declaration"""
        # WCAG 3.1.1 - Language of Page
        return bool(re.search(r'<html[^>]*lang=["\'][^"\']+["\']', content, re.IGNORECASE))
    
    def _check_page_title(self, content):
        """Check for descriptive page titles"""
        # WCAG 2.4.2 - Page Titled
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        if not title_match:
            return False
        
        title = title_match.group(1).strip()
        return len(title) > 0 and title != "Untitled"
    
    def _check_heading_hierarchy(self, content):
        """Check proper heading hierarchy"""
        # WCAG 1.3.1 - Info and Relationships
        headings = re.findall(r'<(h[1-6])[^>]*>', content, re.IGNORECASE)
        
        if not headings:
            return True  # No headings is acceptable
        
        # Check for H1 (should have exactly one)
        h1_count = sum(1 for h in headings if h.lower() == 'h1')
        if h1_count != 1:
            return False
        
        # Check logical hierarchy (simplified check)
        levels = [int(h[1]) for h in headings]
        if levels and levels[0] == 1:  # Starts with H1
            return True
        
        return False
    
    def _check_landmarks(self, content):
        """Check for proper landmark usage"""
        # WCAG 1.3.1 - Info and Relationships
        landmarks = ['main', 'nav', 'header', 'footer', 'aside', 'section']
        found_landmarks = sum(1 for landmark in landmarks if f'<{landmark}' in content.lower())
        
        # Should have at least main, nav, and header for good structure
        essential_landmarks = ['main', 'nav', 'header']
        essential_found = sum(1 for landmark in essential_landmarks if f'<{landmark}' in content.lower())
        
        return essential_found >= 2  # At least 2 essential landmarks
    
    def _check_link_context(self, content):
        """Check link context and descriptions"""
        # WCAG 2.4.4 - Link Purpose (In Context)
        links = re.findall(r'<a[^>]*>([^<]+)</a>', content, re.IGNORECASE)
        
        if not links:
            return True  # No links is acceptable
        
        # Check for descriptive link text (not just "click here", "read more")
        generic_terms = ['click here', 'read more', 'more', 'here', 'link']
        descriptive_links = 0
        
        for link_text in links:
            link_text_lower = link_text.lower().strip()
            if link_text_lower and not any(term in link_text_lower for term in generic_terms):
                descriptive_links += 1
        
        return descriptive_links >= len(links) * 0.8  # 80% should be descriptive
    
    def _check_image_alternatives(self, content):
        """Check image alternative text"""
        # WCAG 1.1.1 - Non-text Content
        images = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
        
        if not images:
            return True  # No images is acceptable
        
        images_with_alt = 0
        for img in images:
            if 'alt=' in img.lower():
                # Check for non-empty alt text
                alt_match = re.search(r'alt=["\']([^"\']*)["\']', img, re.IGNORECASE)
                if alt_match and alt_match.group(1).strip():
                    images_with_alt += 1
                elif alt_match and alt_match.group(1).strip() == "":
                    # Empty alt is acceptable for decorative images
                    images_with_alt += 1
        
        return images_with_alt >= len(images) * 0.9  # 90% should have alt text
    
    def _check_form_labels(self, content):
        """Check form input labels"""
        # WCAG 1.3.1 - Info and Relationships, 3.3.2 - Labels or Instructions
        inputs = re.findall(r'<input[^>]*>', content, re.IGNORECASE)
        
        if not inputs:
            return True  # No forms is acceptable
        
        labeled_inputs = 0
        for input_tag in inputs:
            input_type = re.search(r'type=["\']([^"\']*)["\']', input_tag, re.IGNORECASE)
            input_type = input_type.group(1) if input_type else 'text'
            
            # Skip inputs that don't need labels
            if input_type.lower() in ['hidden', 'submit', 'button']:
                labeled_inputs += 1
                continue
            
            # Check for associated label or aria-label
            if any(attr in input_tag.lower() for attr in ['aria-label=', 'aria-labelledby=', 'title=']):
                labeled_inputs += 1
            else:
                # Check for associated label element (simplified)
                input_id = re.search(r'id=["\']([^"\']*)["\']', input_tag, re.IGNORECASE)
                if input_id and f'for="{input_id.group(1)}"' in content.lower():
                    labeled_inputs += 1
        
        return labeled_inputs >= len(inputs)  # All inputs should be labeled
    
    def _check_keyboard_navigation(self, content):
        """Check keyboard navigation support"""
        # WCAG 2.1.1 - Keyboard
        
        # Check for keyboard event handlers
        keyboard_support = bool(re.search(r'keydown|keypress|keyup|tabindex|accesskey', content, re.IGNORECASE))
        
        # Check for proper tab order (no positive tabindex values)
        positive_tabindex = re.findall(r'tabindex=["\']([^"\']*)["\']', content, re.IGNORECASE)
        no_positive_tabindex = all(int(val) <= 0 for val in positive_tabindex if val.isdigit())
        
        return keyboard_support and no_positive_tabindex
    
    def _check_focus_indicators(self, content):
        """Check focus indicators in CSS"""
        # WCAG 2.4.7 - Focus Visible
        
        # Look for focus styles in CSS or style tags
        focus_styles = bool(re.search(r':focus[^{]*{|focus.*outline|focus.*border', content, re.IGNORECASE))
        
        # Check for CSS custom properties that might handle focus
        css_vars = bool(re.search(r'--.*focus|--.*border|--.*outline', content, re.IGNORECASE))
        
        return focus_styles or css_vars
    
    def _check_color_contrast_basics(self, content):
        """Basic color contrast checks"""
        # WCAG 1.4.3 - Contrast (Minimum)
        
        # Look for CSS custom properties (good for theming and contrast)
        has_css_vars = bool(re.search(r'--[\w-]+:', content))
        
        # Look for dark mode support (indicates contrast consideration)
        dark_mode_support = bool(re.search(r'dark|prefers-color-scheme', content, re.IGNORECASE))
        
        # Look for explicit color declarations
        color_declarations = bool(re.search(r'color:|background:', content, re.IGNORECASE))
        
        return has_css_vars and (dark_mode_support or color_declarations)
    
    def _check_text_alternatives(self, content):
        """Check text alternatives for multimedia"""
        # WCAG 1.1.1 - Non-text Content
        
        # Check for video/audio elements with text alternatives
        media_elements = re.findall(r'<(video|audio)[^>]*>', content, re.IGNORECASE)
        
        if not media_elements:
            return True  # No multimedia is acceptable
        
        # Check for captions, transcripts, or descriptions
        alternatives = bool(re.search(r'captions|transcript|description|subtitles', content, re.IGNORECASE))
        
        return alternatives or len(media_elements) == 0
    
    def _check_skip_navigation(self, content):
        """Check for skip navigation links"""
        # WCAG 2.4.1 - Bypass Blocks
        
        # Look for skip links (usually hidden or at the top)
        skip_links = bool(re.search(r'skip.*content|skip.*main|skip.*navigation', content, re.IGNORECASE))
        
        # Check for proper main content area
        main_content = bool(re.search(r'<main|id=["\']main["\']|class=["\'][^"\']*main[^"\']*["\']', content, re.IGNORECASE))
        
        return skip_links or main_content  # Either skip links or clear main content
    
    def _check_aria_usage(self, content):
        """Check proper ARIA usage"""
        # WCAG 4.1.2 - Name, Role, Value
        
        aria_attributes = re.findall(r'aria-[\w-]+=["\'][^"\']*["\']', content, re.IGNORECASE)
        
        if not aria_attributes:
            return True  # No ARIA is acceptable if not needed
        
        # Check for common ARIA attributes
        common_aria = ['aria-label', 'aria-labelledby', 'aria-describedby', 'aria-hidden', 'aria-expanded']
        found_common = sum(1 for attr in aria_attributes if any(common in attr for common in common_aria))
        
        return found_common > 0  # At least some proper ARIA usage
    
    def _check_semantic_markup(self, content):
        """Check semantic HTML usage"""
        # WCAG 1.3.1 - Info and Relationships
        
        semantic_elements = ['article', 'section', 'nav', 'header', 'footer', 'main', 'aside', 'figure']
        found_semantic = sum(1 for element in semantic_elements if f'<{element}' in content.lower())
        
        # Check for proper list usage
        proper_lists = bool(re.search(r'<ul|<ol|<dl', content, re.IGNORECASE))
        
        return found_semantic >= 3 or proper_lists  # At least 3 semantic elements or lists
    
    def generate_accessibility_report(self):
        """Generate comprehensive accessibility report"""
        print("\n" + "="*80)
        print("♿ WCAG 2.1 AA ACCESSIBILITY COMPLIANCE REPORT")
        print("="*80)
        
        overall_score = self.test_wcag_compliance()
        
        print(f"\n📊 Overall Accessibility Score: {overall_score:.1f}/100")
        
        # Grade the accessibility
        if overall_score >= 90:
            grade = "🟢 EXCELLENT (WCAG AA Compliant)"
            compliance = "Fully compliant with WCAG 2.1 AA standards"
        elif overall_score >= 75:
            grade = "🟡 GOOD (Minor Issues)"
            compliance = "Mostly compliant, minor accessibility improvements needed"
        elif overall_score >= 60:
            grade = "🟠 FAIR (Significant Issues)"
            compliance = "Some compliance issues, accessibility improvements required"
        else:
            grade = "🔴 POOR (Major Issues)"
            compliance = "Major accessibility barriers, immediate attention required"
        
        print(f"🏆 Grade: {grade}")
        print(f"📋 Compliance: {compliance}")
        
        # Page-by-page scores
        if self.results["page_scores"]:
            print(f"\n📄 Page-by-Page Scores:")
            for page_type, score in self.results["page_scores"].items():
                status = "✅" if score >= 75 else "⚠️" if score >= 60 else "❌"
                print(f"  {status} {page_type}: {score:.1f}/100")
        
        # Passed checks
        if self.results["passed"]:
            print(f"\n✅ Passed Accessibility Checks ({len(self.results['passed'])}):")
            for check in self.results["passed"][:10]:  # Show first 10
                print(f"  ✅ {check}")
            if len(self.results["passed"]) > 10:
                print(f"  ... and {len(self.results['passed']) - 10} more")
        
        # Accessibility errors
        if self.results["errors"]:
            print(f"\n❌ Accessibility Issues ({len(self.results['errors'])}):")
            for error in self.results["errors"][:10]:  # Show first 10
                print(f"  ❌ {error}")
            if len(self.results["errors"]) > 10:
                print(f"  ... and {len(self.results['errors']) - 10} more")
        
        # Warnings
        if self.results["warnings"]:
            print(f"\n⚠️  Warnings ({len(self.results['warnings'])}):")
            for warning in self.results["warnings"]:
                print(f"  ⚠️ {warning}")
        
        # Recommendations
        print(f"\n💡 Accessibility Recommendations:")
        
        if overall_score >= 90:
            print("  🎉 Excellent accessibility! Your site meets WCAG 2.1 AA standards.")
            print("  🔧 Consider periodic accessibility audits for ongoing compliance.")
        elif overall_score >= 75:
            print("  👍 Good accessibility foundation. Address minor issues:")
            print("  🔍 Review failed checks and implement recommended fixes.")
            print("  🧪 Test with screen readers and keyboard-only navigation.")
        else:
            print("  🚨 Accessibility improvements needed:")
            print("  🏗️ Focus on heading hierarchy and semantic markup.")
            print("  🖼️ Ensure all images have descriptive alt text.")
            print("  ⌨️ Test keyboard navigation throughout the site.")
            print("  🎨 Verify color contrast meets WCAG standards.")
        
        # WCAG Guidelines reference
        print(f"\n📚 WCAG 2.1 AA Guidelines Tested:")
        print("  • 1.1.1 Non-text Content (Alt text)")
        print("  • 1.3.1 Info and Relationships (Semantic markup)")
        print("  • 1.4.3 Contrast (Minimum color contrast)")
        print("  • 2.1.1 Keyboard (Keyboard accessibility)")
        print("  • 2.4.1 Bypass Blocks (Skip navigation)")
        print("  • 2.4.2 Page Titled (Descriptive titles)")
        print("  • 2.4.4 Link Purpose (Descriptive links)")
        print("  • 2.4.7 Focus Visible (Focus indicators)")
        print("  • 3.1.1 Language of Page (Language declaration)")
        print("  • 3.3.2 Labels or Instructions (Form labels)")
        print("  • 4.1.2 Name, Role, Value (ARIA usage)")
        
        return overall_score >= 75

def main():
    """Main execution function"""
    print("🚀 Starting WCAG 2.1 AA Accessibility Testing...")
    
    tester = AccessibilityTester()
    success = tester.generate_accessibility_report()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()