#!/usr/bin/env python3
"""
Complete Validation Test Runner
Phase 3.9: Content Validation & Testing
Runs all validation tests and generates consolidated report
"""

import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path

class ValidationRunner:
    def __init__(self):
        self.results = {}
        self.overall_status = "unknown"
        
    def run_test(self, test_name, script_name, description):
        """Run a single test script"""
        print(f"\n{'='*60}")
        print(f"🧪 Running {test_name}")
        print(f"📝 {description}")
        print('='*60)
        
        try:
            result = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            self.results[test_name] = {
                "exit_code": result.returncode,
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "description": description
            }
            
            # Print the output
            if result.stdout:
                print(result.stdout)
            if result.stderr and result.returncode != 0:
                print(f"❌ Error: {result.stderr}")
                
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout: {test_name} took longer than 2 minutes")
            self.results[test_name] = {
                "exit_code": -1,
                "success": False,
                "error": "Timeout",
                "description": description
            }
            return False
        except Exception as e:
            print(f"💥 Exception: {e}")
            self.results[test_name] = {
                "exit_code": -1,
                "success": False,
                "error": str(e),
                "description": description
            }
            return False
    
    def run_all_validations(self):
        """Run all validation tests"""
        print("🚀 Starting Complete Site Validation & Testing")
        print("⏰ Started:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Define all tests
        tests = [
            ("hugo_build", "hugo", "Hugo Build Verification"),
            ("content_validation", "validate_content.py", "Content Structure & Quality"),
            ("site_testing", "test_site.py", "Comprehensive Site Testing"), 
            ("link_checking", "check_links.py", "Internal Link Validation"),
            ("seo_performance", "seo_performance_test.py", "SEO & Performance Analysis")
        ]
        
        # Special case for Hugo build
        print(f"\n{'='*60}")
        print(f"🧪 Running Hugo Build")
        print(f"📝 Hugo Build Verification")
        print('='*60)
        
        try:
            hugo_result = subprocess.run(
                ["hugo", "--minify"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            self.results["hugo_build"] = {
                "exit_code": hugo_result.returncode,
                "success": hugo_result.returncode == 0,
                "stdout": hugo_result.stdout,
                "stderr": hugo_result.stderr,
                "description": "Hugo Build Verification"
            }
            
            if hugo_result.returncode == 0:
                print("✅ Hugo build successful")
                print(hugo_result.stdout)
            else:
                print("❌ Hugo build failed")
                print(hugo_result.stderr)
                
        except Exception as e:
            print(f"💥 Hugo build exception: {e}")
            self.results["hugo_build"] = {
                "exit_code": -1,
                "success": False,
                "error": str(e),
                "description": "Hugo Build Verification"
            }
        
        # Run Python test scripts
        python_tests = tests[1:]  # Skip hugo_build since we handled it
        
        for test_name, script_name, description in python_tests:
            # Check if script exists
            if not Path(script_name).exists():
                print(f"⚠️  Skipping {test_name} - script {script_name} not found")
                continue
                
            self.run_test(test_name, script_name, description)
        
        # Generate consolidated report
        self.generate_consolidated_report()
        
        return self.calculate_overall_success()
    
    def calculate_overall_success(self):
        """Calculate overall validation success"""
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results.values() if r.get("success", False))
        
        success_rate = successful_tests / total_tests if total_tests > 0 else 0
        
        if success_rate >= 0.9:
            self.overall_status = "excellent"
        elif success_rate >= 0.7:
            self.overall_status = "good"
        elif success_rate >= 0.5:
            self.overall_status = "fair"
        else:
            self.overall_status = "poor"
        
        return success_rate >= 0.7  # 70% success threshold
    
    def generate_consolidated_report(self):
        """Generate consolidated validation report"""
        print(f"\n{'='*80}")
        print("📊 CONSOLIDATED VALIDATION & TESTING REPORT")
        print('='*80)
        
        # Calculate stats
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results.values() if r.get("success", False))
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Status indicators
        status_indicators = {
            "excellent": "🟢 EXCELLENT",
            "good": "🟡 GOOD", 
            "fair": "🟠 FAIR",
            "poor": "🔴 POOR"
        }
        
        print(f"\n📈 Overall Status: {status_indicators.get(self.overall_status, '❓ UNKNOWN')}")
        print(f"📊 Success Rate: {success_rate:.1f}% ({successful_tests}/{total_tests} tests passed)")
        
        # Individual test results
        print(f"\n🧪 Individual Test Results:")
        print("-" * 60)
        
        for test_name, result in self.results.items():
            status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
            description = result.get("description", "No description")
            print(f"  {status} | {test_name.replace('_', ' ').title()}")
            print(f"         {description}")
            
            if not result.get("success", False):
                error = result.get("error", result.get("stderr", "Unknown error"))
                if error:
                    print(f"         Error: {error}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        
        if self.overall_status == "excellent":
            print("  🎉 Outstanding! Your site passes all validation checks.")
            print("  🚀 Ready for production deployment.")
        elif self.overall_status == "good":
            print("  👍 Good job! Minor issues to address:")
            print("  📝 Review failed tests and fix any critical issues.")
        elif self.overall_status == "fair":
            print("  ⚠️  Several issues need attention:")
            print("  🔧 Address failed tests before production deployment.")
        else:
            print("  🚨 Critical issues found:")
            print("  🛠️  Fix failed tests immediately before deployment.")
        
        print(f"\n🔍 Next Steps:")
        print("  1. Review individual test outputs above")
        print("  2. Address any failed validations")
        print("  3. Re-run tests after fixes")
        print("  4. Deploy once all critical tests pass")
        
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"validation_summary_{timestamp}.json"
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": self.overall_status,
            "success_rate": success_rate,
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "test_results": self.results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        print(f"\n{'='*80}")
        print("⏰ Completed:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        return True

def main():
    """Main execution function"""
    runner = ValidationRunner()
    success = runner.run_all_validations()
    
    print(f"\n🏁 Validation Suite Complete")
    if success:
        print("✅ Overall validation PASSED - Site ready for production!")
        sys.exit(0)
    else:
        print("❌ Overall validation FAILED - Address issues before deployment")
        sys.exit(1)

if __name__ == "__main__":
    main()