"""
Test script to demonstrate CI reliability analysis with mock data
"""

from github.history import calculate_stability_metrics, detect_flakiness


def test_flaky_check():
    """Test detection of a flaky check"""
    print("=== Test Case 1: Flaky Check (alternating outcomes) ===")
    outcomes = [
        {"sha": "a1", "outcome": "PASS"},
        {"sha": "a2", "outcome": "FAIL"},
        {"sha": "a3", "outcome": "PASS"},
        {"sha": "a4", "outcome": "FAIL"},
        {"sha": "a5", "outcome": "PASS"},
    ]
    
    metrics = calculate_stability_metrics(outcomes)
    print(f"Classification: {metrics['classification']}")
    print(f"Stability Score: {metrics['stability_score']}/100")
    print(f"Explanation: {metrics['explanation']}")
    print(f"Is Flaky: {detect_flakiness(outcomes)}")
    print()


def test_reliable_check():
    """Test detection of a reliable check"""
    print("=== Test Case 2: Reliable Check (no failures in 10+ runs) ===")
    outcomes = [{"sha": f"b{i}", "outcome": "PASS"} for i in range(12)]
    
    metrics = calculate_stability_metrics(outcomes)
    print(f"Classification: {metrics['classification']}")
    print(f"Stability Score: {metrics['stability_score']}/100")
    print(f"Explanation: {metrics['explanation']}")
    print(f"Is Flaky: {detect_flakiness(outcomes)}")
    print()


def test_stable_check():
    """Test detection of a stable check"""
    print("=== Test Case 3: Stable Check (3+ consecutive passes) ===")
    outcomes = [
        {"sha": "c1", "outcome": "FAIL"},
        {"sha": "c2", "outcome": "FAIL"},
        {"sha": "c3", "outcome": "PASS"},
        {"sha": "c4", "outcome": "PASS"},
        {"sha": "c5", "outcome": "PASS"},
        {"sha": "c6", "outcome": "PASS"},
    ]
    
    metrics = calculate_stability_metrics(outcomes)
    print(f"Classification: {metrics['classification']}")
    print(f"Stability Score: {metrics['stability_score']}/100")
    print(f"Explanation: {metrics['explanation']}")
    print(f"Is Flaky: {detect_flakiness(outcomes)}")
    print()


def test_unstable_check():
    """Test detection of an unstable check"""
    print("=== Test Case 4: Unstable Check (all failures) ===")
    outcomes = [{"sha": f"d{i}", "outcome": "FAIL"} for i in range(8)]
    
    metrics = calculate_stability_metrics(outcomes)
    print(f"Classification: {metrics['classification']}")
    print(f"Stability Score: {metrics['stability_score']}/100")
    print(f"Explanation: {metrics['explanation']}")
    print(f"Is Flaky: {detect_flakiness(outcomes)}")
    print()


def test_insufficient_data():
    """Test with insufficient data"""
    print("=== Test Case 5: Insufficient Data (< 5 runs) ===")
    outcomes = [
        {"sha": "e1", "outcome": "PASS"},
        {"sha": "e2", "outcome": "FAIL"},
        {"sha": "e3", "outcome": "PASS"},
    ]
    
    metrics = calculate_stability_metrics(outcomes)
    print(f"Classification: {metrics['classification']}")
    print(f"Stability Score: {metrics['stability_score']}/100")
    print(f"Explanation: {metrics['explanation']}")
    print(f"Is Flaky: {detect_flakiness(outcomes)}")
    print()


def test_moderate_pass_rate():
    """Test with moderate pass rate"""
    print("=== Test Case 6: Unstable Check (60% pass rate) ===")
    outcomes = [
        {"sha": f"f{i}", "outcome": "PASS" if i % 5 != 0 else "FAIL"}
        for i in range(10)
    ]
    
    metrics = calculate_stability_metrics(outcomes)
    print(f"Classification: {metrics['classification']}")
    print(f"Stability Score: {metrics['stability_score']}/100")
    print(f"Explanation: {metrics['explanation']}")
    print(f"Total runs: {metrics['total_runs']}, Passes: {metrics['passes']}, Fails: {metrics['failures']}")
    print(f"Is Flaky: {detect_flakiness(outcomes)}")
    print()


if __name__ == "__main__":
    print("CI Reliability Analysis - Test Suite\n")
    print("="*60)
    print()
    
    test_flaky_check()
    test_reliable_check()
    test_stable_check()
    test_unstable_check()
    test_insufficient_data()
    test_moderate_pass_rate()
    
    print("="*60)
    print("\nAll test cases completed!")
