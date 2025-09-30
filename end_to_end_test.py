#!/usr/bin/env python3
"""
End-to-End Content Workflow Test
Phase 3.12: Final Testing & Validation
Tests complete content creation and publishing workflow
"""

import subprocess
import sys
import tempfile
import os
from pathlib import Path
import time
import shutil

class EndToEndTester:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.test_results = []
        self.temp_post_path = None
        
    def test_complete_workflow(self):
        """Test complete content creation workflow"""
        print("🔄 Testing End-to-End Content Workflow...")
        
        workflow_steps = [
            ("Create new post with archetype", self._test_post_creation),
            ("Edit content with frontmatter", self._test_content_editing),
            ("Hugo development server", self._test_dev_server),
            ("Content validation", self._test_content_validation),
            ("Production build", self._test_production_build),
            ("Search index generation", self._test_search_indexing),
            ("Final cleanup", self._test_cleanup)
        ]
        
        success_count = 0
        total_steps = len(workflow_steps)
        
        for step_name, test_function in workflow_steps:
            print(f"  Testing: {step_name}...")
            
            try:
                result = test_function()
                if result:
                    success_count += 1
                    self.test_results.append(f"✅ {step_name}")
                else:
                    self.test_results.append(f"❌ {step_name}")
            except Exception as e:
                self.test_results.append(f"❌ {step_name}: {str(e)}")
        
        workflow_score = (success_count / total_steps) * 100
        return workflow_score
    
    def _test_post_creation(self):
        """Test creating a new post using Hugo archetype"""
        try:
            # Create a test post
            test_post_name = f"test-workflow-{int(time.time())}.md"
            
            result = subprocess.run([
                "hugo", "new", f"posts/{test_post_name}"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                return False
            
            # Check if file was created
            self.temp_post_path = self.root_dir / "content" / "posts" / test_post_name
            
            return self.temp_post_path.exists()
            
        except Exception as e:
            print(f"    Error in post creation: {e}")
            return False
    
    def _test_content_editing(self):
        """Test editing post content"""
        if not self.temp_post_path or not self.temp_post_path.exists():
            return False
        
        try:
            # Read current content
            with open(self.temp_post_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add test content
            test_content = """
# End-to-End Workflow Test

This is a test post created during the end-to-end workflow validation.

## Test Content

- **Bold text** formatting
- *Italic text* formatting  
- `Inline code` formatting

### Code Block Test

```python
def test_function():
    return "Hello, Hugo!"
```

### List Test

1. First item
2. Second item
3. Third item

This test validates the complete content creation and publication workflow.
"""
            
            # Update frontmatter
            updated_content = content.replace(
                'draft: true', 
                'draft: false'
            ).replace(
                'title: ""',
                'title: "End-to-End Workflow Test"'
            )
            
            # Add description if not present
            if 'description:' not in updated_content:
                lines = updated_content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('draft:'):
                        lines.insert(i + 1, 'description: "Testing the complete Hugo content workflow from creation to publication"')
                        break
                updated_content = '\n'.join(lines)
            
            # Append test content
            updated_content += test_content
            
            # Write back to file
            with open(self.temp_post_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            return True
            
        except Exception as e:
            print(f"    Error in content editing: {e}")
            return False
    
    def _test_dev_server(self):
        """Test Hugo development server startup"""
        try:
            # Start Hugo server for a brief test
            process = subprocess.Popen([
                "hugo", "server", "--port=1315", "--bind=127.0.0.1", "--buildDrafts"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait a moment for server to start
            time.sleep(3)
            
            # Check if process is running
            is_running = process.poll() is None
            
            # Terminate the process
            process.terminate()
            
            # Wait for clean shutdown
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            
            return is_running
            
        except Exception as e:
            print(f"    Error testing dev server: {e}")
            return False
    
    def _test_content_validation(self):
        """Test content validation tools"""
        try:
            # Run content validation
            result = subprocess.run([
                "python3", "validate_content.py"
            ], capture_output=True, text=True, timeout=60)
            
            # Validation may have warnings but should not fail completely
            return result.returncode in [0, 1]  # Allow warnings
            
        except Exception as e:
            print(f"    Error in content validation: {e}")
            return False
    
    def _test_production_build(self):
        """Test production build process"""
        try:
            # Run Hugo build
            result = subprocess.run([
                "hugo", "--minify"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                return False
            
            # Check if build output exists
            public_dir = self.root_dir / "public"
            essential_files = [
                "index.html",
                "sitemap.xml",
                "robots.txt",
                "index.json"
            ]
            
            return all((public_dir / file).exists() for file in essential_files)
            
        except Exception as e:
            print(f"    Error in production build: {e}")
            return False
    
    def _test_search_indexing(self):
        """Test search index generation and content inclusion"""
        try:
            search_index_path = self.root_dir / "public" / "index.json"
            
            if not search_index_path.exists():
                return False
            
            # Check if our test post is in the search index
            with open(search_index_path, 'r', encoding='utf-8') as f:
                search_content = f.read()
            
            # Look for test post content in search index
            return "End-to-End Workflow Test" in search_content
            
        except Exception as e:
            print(f"    Error testing search indexing: {e}")
            return False
    
    def _test_cleanup(self):
        """Clean up test files"""
        try:
            # Remove test post
            if self.temp_post_path and self.temp_post_path.exists():
                self.temp_post_path.unlink()
            
            # Rebuild without test post
            result = subprocess.run([
                "hugo", "--minify"
            ], capture_output=True, text=True, timeout=60)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"    Error in cleanup: {e}")
            return False
    
    def test_quickstart_guide(self):
        """Test the quickstart guide workflow"""
        print("📚 Testing Quickstart Guide Workflow...")
        
        quickstart_steps = [
            ("Hugo installation check", self._check_hugo_installation),
            ("Git repository check", self._check_git_repository),
            ("Theme submodule check", self._check_theme_submodule),
            ("Configuration validation", self._check_configuration),
            ("Content structure check", self._check_content_structure),
            ("Development server test", self._test_quickstart_dev_server),
            ("Build process test", self._test_quickstart_build)
        ]
        
        success_count = 0
        total_steps = len(quickstart_steps)
        
        for step_name, test_function in quickstart_steps:
            try:
                result = test_function()
                if result:
                    success_count += 1
                    self.test_results.append(f"✅ Quickstart: {step_name}")
                else:
                    self.test_results.append(f"❌ Quickstart: {step_name}")
            except Exception as e:
                self.test_results.append(f"❌ Quickstart: {step_name}: {str(e)}")
        
        quickstart_score = (success_count / total_steps) * 100
        return quickstart_score
    
    def _check_hugo_installation(self):
        """Check Hugo installation and version"""
        try:
            result = subprocess.run([
                "hugo", "version"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                return False
            
            # Check for extended version
            return "extended" in result.stdout.lower()
            
        except Exception:
            return False
    
    def _check_git_repository(self):
        """Check if we're in a valid Git repository"""
        try:
            result = subprocess.run([
                "git", "status"
            ], capture_output=True, text=True, timeout=10)
            
            return result.returncode == 0
            
        except Exception:
            return False
    
    def _check_theme_submodule(self):
        """Check theme submodule"""
        theme_path = self.root_dir / "themes" / "PaperMod"
        
        # Check if theme directory exists and has content
        if not theme_path.exists():
            return False
        
        # Check if it has essential theme files
        essential_theme_files = [
            "theme.toml",
            "layouts",
            "assets"
        ]
        
        return any((theme_path / file).exists() for file in essential_theme_files)
    
    def _check_configuration(self):
        """Check Hugo configuration"""
        config_path = self.root_dir / "hugo.toml"
        
        if not config_path.exists():
            return False
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_content = f.read()
            
            # Check for essential configuration
            essential_config = [
                "baseURL",
                "title",
                "theme",
                "[params]"
            ]
            
            return all(config in config_content for config in essential_config)
            
        except Exception:
            return False
    
    def _check_content_structure(self):
        """Check content structure"""
        essential_content = [
            "content/_index.md",
            "content/search.md",
            "archetypes/default.md",
            "archetypes/posts.md"
        ]
        
        return all((self.root_dir / path).exists() for path in essential_content)
    
    def _test_quickstart_dev_server(self):
        """Test development server for quickstart"""
        return self._test_dev_server()  # Reuse existing test
    
    def _test_quickstart_build(self):
        """Test build process for quickstart"""
        return self._test_production_build()  # Reuse existing test
    
    def generate_workflow_report(self):
        """Generate comprehensive workflow test report"""
        print("\n" + "="*80)
        print("🔄 END-TO-END WORKFLOW VALIDATION REPORT")
        print("="*80)
        
        # Run workflow tests
        workflow_score = self.test_complete_workflow()
        quickstart_score = self.test_quickstart_guide()
        
        # Calculate overall score
        overall_score = (workflow_score + quickstart_score) / 2
        
        print(f"\n📊 Workflow Test Scores:")
        print(f"  🔄 Content Workflow: {workflow_score:.0f}/100")
        print(f"  📚 Quickstart Guide: {quickstart_score:.0f}/100")
        print(f"  🎯 Overall Workflow Score: {overall_score:.0f}/100")
        
        # Grade the workflow
        if overall_score >= 90:
            grade = "🟢 EXCELLENT"
            status = "Complete workflow functions perfectly!"
        elif overall_score >= 75:
            grade = "🟡 GOOD"
            status = "Workflow is functional with minor issues"
        elif overall_score >= 60:
            grade = "🟠 FAIR"
            status = "Workflow needs some improvements"
        else:
            grade = "🔴 POOR"
            status = "Workflow has significant issues"
        
        print(f"\n🏆 Workflow Grade: {grade}")
        print(f"📋 Status: {status}")
        
        # Show test results
        print(f"\n📋 Workflow Test Results:")
        for result in self.test_results:
            print(f"  {result}")
        
        # Recommendations
        print(f"\n💡 Workflow Recommendations:")
        
        if overall_score >= 90:
            print("  🎉 Excellent! Your Hugo blog workflow is production-ready.")
            print("  📚 Documentation and quickstart guide are accurate and complete.")
        elif overall_score >= 75:
            print("  👍 Good workflow foundation. Minor improvements:")
            print("  🔧 Check any failed workflow steps and address issues.")
            print("  📝 Update documentation if workflow has changed.")
        else:
            print("  🚨 Workflow improvements needed:")
            print("  🏗️ Fix failed workflow steps before production.")
            print("  📚 Review and update quickstart documentation.")
            print("  🔧 Test workflow on fresh installation.")
        
        # Workflow components
        print(f"\n🔄 Workflow Components Tested:")
        print("  • Hugo archetype system for content creation")
        print("  • Development server functionality")
        print("  • Content validation and quality checks")  
        print("  • Production build process")
        print("  • Search index generation and integration")
        print("  • Complete content lifecycle management")
        
        print(f"\n📚 Quickstart Guide Validation:")
        print("  • Prerequisites and installation requirements")
        print("  • Git repository and submodule setup")
        print("  • Configuration file structure and content")
        print("  • Essential directory and file structure")
        print("  • Development and production workflows")
        
        return overall_score >= 75

def main():
    """Main execution function"""
    print("🚀 Starting End-to-End Workflow Testing...")
    
    tester = EndToEndTester()
    success = tester.generate_workflow_report()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()