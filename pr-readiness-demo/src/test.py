"""
Comprehensive test suite for CI Reliability & Flakiness Analytics
All tests in one file for simplicity
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from parser import parse_pr_url
from github.ci import aggregate_ci
from github.confidence import calculate_confidence_score


class TestRunner:
    """Simple test runner without external dependencies"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name, func):
        """Run a single test"""
        try:
            func()
            print(f"✅ {name}")
            self.passed += 1
            return True
        except AssertionError as e:
            print(f"❌ {name}: {e}")
            self.failed += 1
            return False
        except Exception as e:
            print(f"❌ {name}: Unexpected error: {e}")
            self.failed += 1
            return False
    
    def summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        print()
        print("="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"✅ Passed: {self.passed}/{total}")
        print(f"❌ Failed: {self.failed}/{total}")
        if self.failed == 0:
            print()
            print("🎉 ALL TESTS PASSED!")
        print("="*70)
        return self.failed == 0


# ============================================================================
# PARSER TESTS
# ============================================================================

def test_valid_pr_url():
    """Test parsing a valid PR URL"""
    result = parse_pr_url("https://github.com/zulip/zulip/pull/37753")
    assert result["owner"] == "zulip"
    assert result["repo"] == "zulip"
    assert result["number"] == "37753"

def test_valid_pr_url_with_hyphens():
    """Test parsing URL with hyphens in names"""
    result = parse_pr_url("https://github.com/OWASP-BLT/BLT/pull/5618")
    assert result["owner"] == "OWASP-BLT"
    assert result["repo"] == "BLT"
    assert result["number"] == "5618"

def test_valid_pr_url_trailing_slash():
    """Test parsing URL with trailing slash"""
    result = parse_pr_url("https://github.com/owner/repo/pull/123/")
    assert result["owner"] == "owner"
    assert result["repo"] == "repo"
    assert result["number"] == "123"

def test_invalid_url_not_github():
    """Test that non-GitHub URLs are rejected"""
    try:
        parse_pr_url("https://gitlab.com/owner/repo/pull/123")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_invalid_url_not_pr():
    """Test that non-PR GitHub URLs are rejected"""
    try:
        parse_pr_url("https://github.com/owner/repo/issues/123")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_invalid_url_malformed():
    """Test that malformed URLs are rejected"""
    try:
        parse_pr_url("not-a-url")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# ============================================================================
# CI AGGREGATION TESTS
# ============================================================================

def test_no_ci_checks():
    """Test PR with no CI checks"""
    state, details = aggregate_ci([], [])
    assert state == "NO_CI"
    assert details == []

def test_all_passing_checks():
    """Test PR where all CI checks pass"""
    check_runs = [
        {"name": "test1", "status": "completed", "conclusion": "success"},
        {"name": "test2", "status": "completed", "conclusion": "success"}
    ]
    statuses = [{"context": "status1", "state": "success"}]
    
    state, details = aggregate_ci(check_runs, statuses)
    assert state == "PASS"
    assert len(details) == 3

def test_one_failing_check():
    """Test PR with one failing check"""
    check_runs = [
        {"name": "test1", "status": "completed", "conclusion": "success"},
        {"name": "test2", "status": "completed", "conclusion": "failure"}
    ]
    
    state, details = aggregate_ci(check_runs, [])
    assert state == "FAIL"

def test_pending_checks():
    """Test PR with pending checks"""
    check_runs = [
        {"name": "test1", "status": "completed", "conclusion": "success"},
        {"name": "test2", "status": "in_progress", "conclusion": None}
    ]
    
    state, details = aggregate_ci(check_runs, [])
    assert state == "PENDING"

def test_fail_priority_over_pending():
    """Test that FAIL takes priority over PENDING"""
    check_runs = [
        {"name": "test1", "status": "completed", "conclusion": "failure"},
        {"name": "test2", "status": "in_progress", "conclusion": None}
    ]
    
    state, details = aggregate_ci(check_runs, [])
    assert state == "FAIL"

def test_cancelled_check():
    """Test cancelled check treated as failure"""
    check_runs = [{"name": "test1", "status": "completed", "conclusion": "cancelled"}]
    state, details = aggregate_ci(check_runs, [])
    assert state == "FAIL"

def test_mixed_check_runs_and_statuses():
    """Test PR with both check runs and commit statuses"""
    check_runs = [{"name": "pytest", "status": "completed", "conclusion": "success"}]
    statuses = [{"context": "codecov", "state": "success"}]
    
    state, details = aggregate_ci(check_runs, statuses)
    assert state == "PASS"
    assert len(details) == 2


# ============================================================================
# CONFIDENCE SCORING TESTS
# ============================================================================

def test_reliable_perfect_record():
    """Test RELIABLE classification for perfect track record"""
    outcomes = [{"outcome": "PASS", "sha": f"sha{i}"} for i in range(10)]
    result = calculate_confidence_score(outcomes)
    
    assert result['classification'] == 'RELIABLE'
    assert result['confidence_score'] >= 90

def test_reliable_high_pass_rate():
    """Test RELIABLE classification for high pass rate"""
    outcomes = [{"outcome": "PASS", "sha": f"sha{i}"} for i in range(14)]
    outcomes.append({"outcome": "FAIL", "sha": "sha14"})
    result = calculate_confidence_score(outcomes)
    
    assert result['classification'] == 'RELIABLE'
    assert result['confidence_score'] >= 90

def test_stable_consecutive_passes():
    """Test STABLE classification for consecutive passes"""
    outcomes = [
        {"outcome": "FAIL", "sha": "sha0"},
        {"outcome": "FAIL", "sha": "sha1"},
        {"outcome": "PASS", "sha": "sha2"},
        {"outcome": "PASS", "sha": "sha3"},
        {"outcome": "PASS", "sha": "sha4"},
        {"outcome": "PASS", "sha": "sha5"}
    ]
    result = calculate_confidence_score(outcomes)
    
    assert result['classification'] == 'STABLE'
    assert 70 <= result['confidence_score'] < 90

def test_flaky_alternating():
    """Test FLAKY classification for alternating outcomes"""
    outcomes = [
        {"outcome": "PASS", "sha": "sha0"},
        {"outcome": "FAIL", "sha": "sha1"},
        {"outcome": "PASS", "sha": "sha2"},
        {"outcome": "FAIL", "sha": "sha3"},
        {"outcome": "PASS", "sha": "sha4"}
    ]
    result = calculate_confidence_score(outcomes)
    
    assert result['classification'] == 'FLAKY'
    assert 20 <= result['confidence_score'] <= 50

def test_unstable_consecutive_failures():
    """Test UNSTABLE classification for consecutive failures"""
    outcomes = [
        {"outcome": "PASS", "sha": "sha0"},
        {"outcome": "FAIL", "sha": "sha1"},
        {"outcome": "FAIL", "sha": "sha2"},
        {"outcome": "FAIL", "sha": "sha3"}
    ]
    result = calculate_confidence_score(outcomes)
    
    assert result['classification'] == 'UNSTABLE'
    assert result['confidence_score'] <= 30

def test_unknown_insufficient_data():
    """Test UNKNOWN classification for insufficient data"""
    outcomes = [
        {"outcome": "PASS", "sha": "sha0"},
        {"outcome": "PASS", "sha": "sha1"}
    ]
    result = calculate_confidence_score(outcomes)
    
    assert result['classification'] == 'UNKNOWN'
    assert 40 <= result['confidence_score'] <= 60


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    """Run all tests"""
    print()
    print("="*70)
    print("CI RELIABILITY & FLAKINESS ANALYTICS - TEST SUITE")
    print("="*70)
    print()
    
    runner = TestRunner()
    
    # Parser tests
    print("📦 Parser Tests")
    print("-" * 70)
    runner.test("Valid PR URL", test_valid_pr_url)
    runner.test("Valid PR URL with hyphens", test_valid_pr_url_with_hyphens)
    runner.test("Valid PR URL with trailing slash", test_valid_pr_url_trailing_slash)
    runner.test("Invalid: Not GitHub", test_invalid_url_not_github)
    runner.test("Invalid: Not PR", test_invalid_url_not_pr)
    runner.test("Invalid: Malformed URL", test_invalid_url_malformed)
    
    print()
    
    # CI Aggregation tests
    print("📦 CI Aggregation Tests")
    print("-" * 70)
    runner.test("No CI checks", test_no_ci_checks)
    runner.test("All passing checks", test_all_passing_checks)
    runner.test("One failing check", test_one_failing_check)
    runner.test("Pending checks", test_pending_checks)
    runner.test("FAIL priority over PENDING", test_fail_priority_over_pending)
    runner.test("Cancelled check treated as failure", test_cancelled_check)
    runner.test("Mixed check runs and statuses", test_mixed_check_runs_and_statuses)
    
    print()
    
    # Confidence Scoring tests
    print("📦 Confidence Scoring Tests")
    print("-" * 70)
    runner.test("RELIABLE: Perfect record", test_reliable_perfect_record)
    runner.test("RELIABLE: High pass rate", test_reliable_high_pass_rate)
    runner.test("STABLE: Consecutive passes", test_stable_consecutive_passes)
    runner.test("FLAKY: Alternating outcomes", test_flaky_alternating)
    runner.test("UNSTABLE: Consecutive failures", test_unstable_consecutive_failures)
    runner.test("UNKNOWN: Insufficient data", test_unknown_insufficient_data)
    
    # Summary
    success = runner.summary()
    
    print()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
