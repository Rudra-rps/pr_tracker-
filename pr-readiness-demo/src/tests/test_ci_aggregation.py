"""
Unit tests for CI aggregation logic
Tests various CI state combinations and edge cases
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from github.ci import aggregate_ci


class TestCIAggregation:
    """Test suite for CI status aggregation"""
    
    def test_no_ci_checks(self):
        """Test PR with no CI checks at all"""
        check_runs = []
        statuses = []
        
        state, details = aggregate_ci(check_runs, statuses)
        
        assert state == "NO_CI"
        assert details == []
    
    def test_all_passing_checks(self):
        """Test PR where all CI checks pass"""
        check_runs = [
            {"name": "test1", "status": "completed", "conclusion": "success"},
            {"name": "test2", "status": "completed", "conclusion": "success"}
        ]
        statuses = [
            {"context": "status1", "state": "success"}
        ]
        
        state, details = aggregate_ci(check_runs, statuses)
        
        assert state == "PASS"
        assert len(details) == 3
    
    def test_one_failing_check(self):
        """Test PR with one failing check"""
        check_runs = [
            {"name": "test1", "status": "completed", "conclusion": "success"},
            {"name": "test2", "status": "completed", "conclusion": "failure"}
        ]
        statuses = []
        
        state, details = aggregate_ci(check_runs, statuses)
        
        assert state == "FAIL"
    
    def test_pending_checks(self):
        """Test PR with pending checks"""
        check_runs = [
            {"name": "test1", "status": "completed", "conclusion": "success"},
            {"name": "test2", "status": "in_progress", "conclusion": None}
        ]
        statuses = []
        
        state, details = aggregate_ci(check_runs, statuses)
        
        assert state == "PENDING"
    
    def test_failed_and_pending(self):
        """Test that FAIL takes priority over PENDING"""
        check_runs = [
            {"name": "test1", "status": "completed", "conclusion": "failure"},
            {"name": "test2", "status": "in_progress", "conclusion": None}
        ]
        statuses = []
        
        state, details = aggregate_ci(check_runs, statuses)
        
        assert state == "FAIL"
    
    def test_cancelled_check(self):
        """Test cancelled check is treated as failure"""
        check_runs = [
            {"name": "test1", "status": "completed", "conclusion": "cancelled"}
        ]
        statuses = []
        
        state, details = aggregate_ci(check_runs, statuses)
        
        assert state == "FAIL"
    
    def test_timed_out_check(self):
        """Test timed out check is treated as failure"""
        check_runs = [
            {"name": "test1", "status": "completed", "conclusion": "timed_out"}
        ]
        statuses = []
        
        state, details = aggregate_ci(check_runs, statuses)
        
        assert state == "FAIL"
    
    def test_error_check(self):
        """Test errored check is treated as failure"""
        check_runs = [
            {"name": "test1", "status": "completed", "conclusion": "error"}
        ]
        statuses = []
        
        state, details = aggregate_ci(check_runs, statuses)
        
        assert state == "FAIL"
    
    def test_only_statuses_no_check_runs(self):
        """Test PR with only commit statuses (legacy CI)"""
        check_runs = []
        statuses = [
            {"context": "ci/travis", "state": "success"},
            {"context": "ci/jenkins", "state": "success"}
        ]
        
        state, details = aggregate_ci(check_runs, statuses)
        
        assert state == "PASS"
        assert len(details) == 2
    
    def test_pending_status(self):
        """Test pending commit status"""
        check_runs = []
        statuses = [
            {"context": "ci/test", "state": "pending"}
        ]
        
        state, details = aggregate_ci(check_runs, statuses)
        
        assert state == "PENDING"
    
    def test_failed_status(self):
        """Test failed commit status"""
        check_runs = []
        statuses = [
            {"context": "ci/test", "state": "failure"}
        ]
        
        state, details = aggregate_ci(check_runs, statuses)
        
        assert state == "FAIL"
    
    def test_mixed_check_runs_and_statuses(self):
        """Test PR with both check runs and commit statuses"""
        check_runs = [
            {"name": "pytest", "status": "completed", "conclusion": "success"}
        ]
        statuses = [
            {"context": "codecov", "state": "success"}
        ]
        
        state, details = aggregate_ci(check_runs, statuses)
        
        assert state == "PASS"
        assert len(details) == 2
        assert any(d["name"] == "pytest" for d in details)
        assert any(d["name"] == "codecov" for d in details)


def run_tests():
    """Run all CI aggregation tests and display results"""
    print("="*70)
    print("CI AGGREGATION UNIT TESTS")
    print("="*70)
    print()
    
    test_suite = TestCIAggregation()
    tests = [
        ("No CI checks", test_suite.test_no_ci_checks),
        ("All passing checks", test_suite.test_all_passing_checks),
        ("One failing check", test_suite.test_one_failing_check),
        ("Pending checks", test_suite.test_pending_checks),
        ("Failed and pending (priority)", test_suite.test_failed_and_pending),
        ("Cancelled check", test_suite.test_cancelled_check),
        ("Timed out check", test_suite.test_timed_out_check),
        ("Error check", test_suite.test_error_check),
        ("Only statuses (legacy CI)", test_suite.test_only_statuses_no_check_runs),
        ("Pending status", test_suite.test_pending_status),
        ("Failed status", test_suite.test_failed_status),
        ("Mixed checks and statuses", test_suite.test_mixed_check_runs_and_statuses),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✅ {name}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {name}: Unexpected error: {e}")
            failed += 1
    
    print()
    print("="*70)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("="*70)
    
    return passed, failed


if __name__ == "__main__":
    run_tests()
