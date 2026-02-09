#!/usr/bin/env python3
"""
Complete Workflow Example: Report Generation at End of Execution

This script demonstrates the complete robotframework-quality-scanner v0.3.0
workflow with automatic report generation at the end of each scan.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from robotframework_quality_scanner import QualityScanner


def main():
    """
    Complete workflow:
    1. Scan files
    2. Generate reports automatically
    3. Access report data
    4. Save to disk
    5. Display summaries
    """
    
    # Initialize scanner
    scanner = QualityScanner()
    
    print("=" * 80)
    print("robotframework-quality-scanner v0.3.0 - Complete Workflow")
    print("=" * 80)
    print()
    
    # Step 1: Scan with automatic report generation
    print("STEP 1: Scanning files...")
    issues, reports = scanner.scan("./examples/bad_web.robot", use_cache=False)
    print(f"✓ Scan completed in {scanner.scan_time:.4f}s")
    print(f"✓ Found {len(issues)} issues")
    print()
    
    # Step 2: Access executive report
    print("STEP 2: Executive Report Summary")
    print("-" * 80)
    executive_dict = reports['executive'].to_dict()
    summary = executive_dict['summary']
    
    print(f"Quality Score: {summary['quality_score']}/100")
    print(f"Total Issues: {summary['total_issues']}")
    print(f"Files Analyzed: {summary['files_analyzed']}")
    print(f"Scan Duration: {summary['scan_time_seconds']:.4f}s")
    print()
    
    print("Severity Breakdown:")
    for severity, count in executive_dict['severity_breakdown'].items():
        print(f"  {severity}: {count}")
    print()
    
    print("Category Breakdown:")
    for category, count in executive_dict['category_breakdown'].items():
        print(f"  {category}: {count}")
    print()
    
    # Step 3: Access coverage report
    print("STEP 3: Coverage Report Summary")
    print("-" * 80)
    coverage_dict = reports['coverage'].to_dict()
    overall = coverage_dict['overall']
    
    print(f"Total Keywords: {overall['total_keywords']}")
    print(f"Documented Keywords: {overall['documented_keywords']}")
    print(f"Used Keywords: {overall['used_keywords']}")
    print(f"Test Cases: {overall['total_tests']}")
    print(f"Documentation Coverage: {overall['documentation_coverage_percent']:.1f}%")
    print(f"Keyword Usage Coverage: {overall['keyword_usage_coverage_percent']:.1f}%")
    print()
    
    # Step 4: Save reports to disk
    print("STEP 4: Saving Reports to Disk")
    print("-" * 80)
    output_dir = scanner.save_reports("./quality-reports")
    print(f"✓ Reports saved to: {output_dir}")
    print()
    print("Generated Files:")
    print("  - executive_report.html (Visual dashboard)")
    print("  - executive_report.txt (Console summary)")
    print("  - executive_report.json (Programmatic access)")
    print("  - coverage_report.html (Coverage visualization)")
    print("  - coverage_report.txt (Coverage summary)")
    print()
    
    # Step 5: Display text reports
    print("STEP 5: Text Report Outputs")
    print("-" * 80)
    print()
    print("Executive Report (Text):")
    print(reports['executive'].to_text())
    print()
    print("Coverage Report (Text):")
    print(reports['coverage'].to_text())
    print()
    
    print("=" * 80)
    print("✓ Complete workflow executed successfully!")
    print("=" * 80)


if __name__ == '__main__':
    main()
