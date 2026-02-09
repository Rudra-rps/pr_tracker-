"""
Test runner for all unit tests
Runs parser, CI aggregation, and confidence scoring tests
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tests.test_parser import run_tests as run_parser_tests
from tests.test_ci_aggregation import run_tests as run_ci_tests


def main():
    """Run all test suites"""
    print()
    print("="*70)
    print("RUNNING ALL UNIT TESTS")
    print("="*70)
    print()
    
    all_passed = 0
    all_failed = 0
    
    # Run parser tests
    print("\n📦 Running Parser Tests...")
    passed, failed = run_parser_tests()
    all_passed += passed
    all_failed += failed
    
    print("\n")
    
    # Run CI aggregation tests
    print("📦 Running CI Aggregation Tests...")
    passed, failed = run_ci_tests()
    all_passed += passed
    all_failed += failed
    
    # Summary
    print()
    print()
    print("="*70)
    print("OVERALL TEST SUMMARY")
    print("="*70)
    print(f"✅ Total Passed: {all_passed}")
    print(f"❌ Total Failed: {all_failed}")
    print(f"📊 Total Tests:  {all_passed + all_failed}")
    
    if all_failed == 0:
        print()
        print("🎉 ALL TESTS PASSED!")
    else:
        print()
        print(f"⚠️  {all_failed} test(s) failed")
    
    print("="*70)
    print()
    
    # Exit with appropriate code
    sys.exit(0 if all_failed == 0 else 1)


if __name__ == "__main__":
    main()
