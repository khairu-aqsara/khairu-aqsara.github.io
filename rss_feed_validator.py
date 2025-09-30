#!/usr/bin/env python3
"""
RSS Feed Validator
Phase 3.12: Final Testing & Validation
Validates RSS feed structure and functionality
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import urllib.parse

class RSSFeedValidator:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.public_dir = self.root_dir / "public"
        self.results = {
            "structure": {"score": 0, "details": []},
            "content": {"score": 0, "details": []},
            "metadata": {"score": 0, "details": []},
            "compliance": {"score": 0, "details": []}
        }
        self.issues = []
        self.warnings = []
        
    def validate_rss_feed(self):
        """Validate RSS feed structure and content"""
        print("📡 Validating RSS Feed...")
        
        rss_path = self.public_dir / "index.xml"
        if not rss_path.exists():
            self.issues.append("RSS feed file (index.xml) not found")
            return 0
        
        try:
            # Parse XML
            tree = ET.parse(rss_path)
            root = tree.getroot()
            
            # Validate structure
            structure_score = self._validate_feed_structure(root)
            
            # Validate content
            content_score = self._validate_feed_content(root)
            
            # Validate metadata
            metadata_score = self._validate_feed_metadata(root)
            
            # Validate RSS compliance
            compliance_score = self._validate_rss_compliance(root)
            
            # Update results
            self.results["structure"]["score"] = structure_score
            self.results["content"]["score"] = content_score
            self.results["metadata"]["score"] = metadata_score
            self.results["compliance"]["score"] = compliance_score
            
            # Calculate overall score
            overall_score = (structure_score + content_score + metadata_score + compliance_score) / 4
            
            return overall_score
            
        except ET.ParseError as e:
            self.issues.append(f"RSS feed XML parsing error: {e}")
            return 0
        except Exception as e:
            self.issues.append(f"Error validating RSS feed: {e}")
            return 0
    
    def _validate_feed_structure(self, root):
        """Validate basic RSS feed structure"""
        score = 0
        
        # Check root element
        if root.tag == 'rss':
            score += 20
            self.results["structure"]["details"].append("Valid RSS root element ✅")
            
            # Check version attribute
            version = root.get('version')
            if version == '2.0':
                score += 10
                self.results["structure"]["details"].append("RSS 2.0 version ✅")
            else:
                self.warnings.append(f"RSS version is {version}, expected 2.0")
        else:
            self.issues.append("Invalid RSS root element")
            return 0
        
        # Check for channel element
        channel = root.find('channel')
        if channel is not None:
            score += 20
            self.results["structure"]["details"].append("Channel element found ✅")
            
            # Check required channel elements
            required_elements = ['title', 'link', 'description']
            found_required = 0
            
            for element in required_elements:
                if channel.find(element) is not None:
                    found_required += 1
                    self.results["structure"]["details"].append(f"Required element '{element}' found ✅")
                else:
                    self.issues.append(f"Missing required element: {element}")
            
            if found_required == len(required_elements):
                score += 30
            else:
                score += (found_required / len(required_elements)) * 30
            
            # Check for items
            items = channel.findall('item')
            if items:
                score += 20
                self.results["structure"]["details"].append(f"Found {len(items)} feed items ✅")
            else:
                self.warnings.append("No items found in RSS feed")
        else:
            self.issues.append("Channel element not found")
        
        return min(score, 100)
    
    def _validate_feed_content(self, root):
        """Validate RSS feed content quality"""
        score = 0
        
        channel = root.find('channel')
        if channel is None:
            return 0
        
        # Validate channel content
        title = channel.find('title')
        if title is not None and title.text and len(title.text.strip()) > 0:
            score += 15
            self.results["content"]["details"].append("Channel title is descriptive ✅")
        
        description = channel.find('description')
        if description is not None and description.text and len(description.text.strip()) > 20:
            score += 15
            self.results["content"]["details"].append("Channel description is detailed ✅")
        
        link = channel.find('link')
        if link is not None and link.text and link.text.startswith('http'):
            score += 10
            self.results["content"]["details"].append("Channel link is valid URL ✅")
        
        # Validate item content
        items = channel.findall('item')
        if not items:
            return score
        
        valid_items = 0
        
        for item in items:
            item_score = 0
            
            # Check required item elements
            item_title = item.find('title')
            if item_title is not None and item_title.text:
                item_score += 5
            
            item_link = item.find('link')
            if item_link is not None and item_link.text and item_link.text.startswith('http'):
                item_score += 5
            
            item_desc = item.find('description')
            if item_desc is not None and item_desc.text and len(item_desc.text.strip()) > 10:
                item_score += 5
            
            # Check for pub date
            pub_date = item.find('pubDate')
            if pub_date is not None and pub_date.text:
                item_score += 5
            
            # Check for GUID
            guid = item.find('guid')
            if guid is not None and guid.text:
                item_score += 5
            
            if item_score >= 15:  # At least 3 out of 5 checks
                valid_items += 1
        
        if items:
            item_quality_ratio = valid_items / len(items)
            score += item_quality_ratio * 60
            
            if item_quality_ratio > 0.8:
                self.results["content"]["details"].append("High-quality item content ✅")
            else:
                self.warnings.append(f"Only {valid_items}/{len(items)} items have complete metadata")
        
        return min(score, 100)
    
    def _validate_feed_metadata(self, root):
        """Validate RSS feed metadata"""
        score = 0
        
        channel = root.find('channel')
        if channel is None:
            return 0
        
        # Check for optional but recommended elements
        metadata_elements = {
            'generator': 15,
            'language': 10,
            'lastBuildDate': 15,
            'managingEditor': 5,
            'webMaster': 5,
            'category': 5,
            'copyright': 5
        }
        
        # Check for Atom namespace and self-link
        atom_link = None
        for child in channel:
            if child.tag.endswith('}link') and child.get('rel') == 'self':
                atom_link = child
                break
        
        if atom_link is not None:
            score += 20
            self.results["metadata"]["details"].append("Atom self-link found ✅")
        
        # Check metadata elements
        for element, points in metadata_elements.items():
            elem = channel.find(element)
            if elem is not None and elem.text:
                score += points
                self.results["metadata"]["details"].append(f"Metadata '{element}' present ✅")
        
        # Check for valid encoding
        try:
            with open(self.public_dir / "index.xml", 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if 'encoding="utf-8"' in first_line.lower():
                    score += 10
                    self.results["metadata"]["details"].append("UTF-8 encoding specified ✅")
        except Exception:
            pass
        
        # Check for proper namespace declarations
        namespaces = []
        for attr_name, attr_value in root.attrib.items():
            if attr_name.startswith('xmlns'):
                namespaces.append(attr_value)
        
        if namespaces:
            score += 10
            self.results["metadata"]["details"].append("XML namespaces declared ✅")
        
        return min(score, 100)
    
    def _validate_rss_compliance(self, root):
        """Validate RSS 2.0 specification compliance"""
        score = 0
        
        # Check RSS 2.0 specification compliance
        channel = root.find('channel')
        if channel is None:
            return 0
        
        # Required elements per RSS 2.0 spec
        required_channel_elements = ['title', 'link', 'description']
        for element in required_channel_elements:
            if channel.find(element) is not None:
                score += 10
        
        # Check item structure compliance
        items = channel.findall('item')
        compliant_items = 0
        
        for item in items:
            # Each item must have either title or description (RSS 2.0 spec)
            has_title = item.find('title') is not None and item.find('title').text
            has_description = item.find('description') is not None and item.find('description').text
            
            if has_title or has_description:
                compliant_items += 1
        
        if items:
            compliance_ratio = compliant_items / len(items)
            score += compliance_ratio * 40
            
            if compliance_ratio == 1.0:
                self.results["compliance"]["details"].append("All items RSS 2.0 compliant ✅")
            else:
                self.warnings.append(f"Only {compliant_items}/{len(items)} items are fully compliant")
        
        # Check for well-formed XML
        try:
            # If we got this far, XML is well-formed
            score += 20
            self.results["compliance"]["details"].append("Well-formed XML structure ✅")
        except Exception:
            self.issues.append("XML is not well-formed")
        
        # Check for valid URLs in links
        valid_links = 0
        total_links = 0
        
        # Check channel link
        channel_link = channel.find('link')
        if channel_link is not None and channel_link.text:
            total_links += 1
            if self._is_valid_url(channel_link.text):
                valid_links += 1
        
        # Check item links
        for item in items:
            item_link = item.find('link')
            if item_link is not None and item_link.text:
                total_links += 1
                if self._is_valid_url(item_link.text):
                    valid_links += 1
        
        if total_links > 0:
            url_validity_ratio = valid_links / total_links
            score += url_validity_ratio * 20
            
            if url_validity_ratio > 0.9:
                self.results["compliance"]["details"].append("Valid URLs in feed ✅")
        
        return min(score, 100)
    
    def _is_valid_url(self, url):
        """Check if URL is valid"""
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
        except Exception:
            return False
    
    def validate_feed_accessibility(self):
        """Validate feed accessibility and discoverability"""
        print("🔍 Validating Feed Accessibility...")
        
        score = 0
        
        # Check if feed is linked from HTML pages
        html_files = list(self.public_dir.glob("*.html"))
        feed_linked = False
        
        for html_file in html_files[:3]:  # Check first 3 HTML files
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for RSS feed links
                if re.search(r'type=["\']application/rss\+xml["\']|href=["\'][^"\']*\.xml["\']', content, re.IGNORECASE):
                    feed_linked = True
                    break
            except Exception:
                continue
        
        if feed_linked:
            score += 50
            self.results["compliance"]["details"].append("RSS feed linked from HTML pages ✅")
        else:
            self.warnings.append("RSS feed not linked from HTML pages")
        
        # Check feed file accessibility
        rss_path = self.public_dir / "index.xml"
        if rss_path.exists():
            score += 30
            self.results["compliance"]["details"].append("RSS feed file accessible ✅")
            
            # Check file size (should be reasonable)
            file_size = rss_path.stat().st_size
            if file_size < 1024 * 1024:  # Less than 1MB
                score += 20
                self.results["compliance"]["details"].append(f"RSS feed size reasonable ({file_size} bytes) ✅")
            else:
                self.warnings.append(f"RSS feed file is large ({file_size} bytes)")
        
        return score
    
    def generate_rss_report(self):
        """Generate comprehensive RSS feed validation report"""
        print("\n" + "="*80)
        print("📡 RSS FEED VALIDATION REPORT")
        print("="*80)
        
        # Run validation
        feed_score = self.validate_rss_feed()
        accessibility_score = self.validate_feed_accessibility()
        
        # Calculate overall RSS score
        overall_score = (feed_score * 0.8 + accessibility_score * 0.2)  # Feed validation is more important
        
        print(f"\n📊 RSS Feed Scores:")
        print(f"  📡 Feed Structure: {self.results['structure']['score']:.0f}/100")
        print(f"  📝 Content Quality: {self.results['content']['score']:.0f}/100")
        print(f"  📋 Metadata: {self.results['metadata']['score']:.0f}/100")
        print(f"  ✅ Compliance: {self.results['compliance']['score']:.0f}/100")
        print(f"  🔍 Accessibility: {accessibility_score:.0f}/100")
        print(f"  🎯 Overall RSS Score: {overall_score:.0f}/100")
        
        # Grade the RSS feed
        if overall_score >= 90:
            grade = "🟢 EXCELLENT"
            status = "RSS feed meets all best practices!"
        elif overall_score >= 75:
            grade = "🟡 GOOD"
            status = "RSS feed is well-structured with minor improvements possible"
        elif overall_score >= 60:
            grade = "🟠 FAIR"
            status = "RSS feed is functional but could be improved"
        else:
            grade = "🔴 POOR"
            status = "RSS feed has significant issues that need attention"
        
        print(f"\n🏆 RSS Grade: {grade}")
        print(f"📋 Status: {status}")
        
        # Show validation details
        print(f"\n✅ RSS Feed Validation Results:")
        for category, data in self.results.items():
            if data["details"]:
                print(f"  {category.replace('_', ' ').title()}:")
                for detail in data["details"]:
                    print(f"    ✅ {detail}")
        
        # Show issues
        if self.issues:
            print(f"\n❌ Issues Found ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  ❌ {issue}")
        
        # Show warnings
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  ⚠️ {warning}")
        
        # Recommendations
        print(f"\n💡 RSS Feed Recommendations:")
        
        if overall_score >= 90:
            print("  🎉 Excellent RSS feed! Your feed follows all best practices.")
            print("  📊 Consider monitoring feed statistics and subscriber engagement.")
        elif overall_score >= 75:
            print("  👍 Good RSS feed foundation. Consider these improvements:")
            print("  📋 Add missing optional metadata elements.")
            print("  🔗 Ensure feed is discoverable from all relevant pages.")
        else:
            print("  🚨 RSS feed improvements needed:")
            print("  📝 Ensure all required elements are present and valid.")
            print("  🔗 Add proper feed discovery links to HTML pages.")
            print("  📊 Validate feed content and metadata completeness.")
            print("  ✅ Test feed in RSS readers and validators.")
        
        # RSS 2.0 specification guidance
        print(f"\n📚 RSS 2.0 Specification Elements:")
        print("  Required: title, link, description (channel)")
        print("  Required: title OR description (items)")
        print("  Recommended: pubDate, guid, author, category")
        print("  Optional: generator, language, lastBuildDate, ttl")
        
        # Feed testing tools
        print(f"\n🔧 RSS Feed Testing Tools:")
        print("  • W3C Feed Validation Service")
        print("  • RSS Reader testing (Feedly, NewsBlur)")
        print("  • Feed statistics and analytics")
        print("  • Podcast feed validators (if applicable)")
        
        return overall_score >= 75

def main():
    """Main execution function"""
    print("🚀 Starting RSS Feed Validation...")
    
    validator = RSSFeedValidator()
    success = validator.generate_rss_report()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()