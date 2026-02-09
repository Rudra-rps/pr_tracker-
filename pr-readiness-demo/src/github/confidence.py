"""
CI Confidence Scoring Engine
Deterministic scoring system for CI reliability with transparent explanations
"""

def calculate_confidence_score(outcomes):
    """
    Calculate a deterministic confidence score (0-100) for a CI check
    
    Scoring Algorithm:
    - RELIABLE (90-100): Consistent passes, no failures
    - STABLE (70-89): Recent stability with good pass rate
    - FLAKY (20-50): Alternating pass/fail patterns
    - UNSTABLE (10-30): Consistent failures or poor pass rate
    - UNKNOWN (40-60): Insufficient data
    
    Args:
        outcomes: List of outcome dicts with 'outcome' field (PASS/FAIL/PENDING)
    
    Returns:
        dict with confidence_score, classification, reason, and metrics
    """
    if not outcomes:
        return {
            "confidence_score": 40,
            "classification": "UNKNOWN",
            "reason": "No historical data available for this check",
            "metrics": {
                "total_runs": 0,
                "passes": 0,
                "failures": 0,
                "pass_rate": 0,
                "consecutive_passes": 0,
                "consecutive_failures": 0,
                "flaky_transitions": 0
            }
        }
    
    # Filter out PENDING status for analysis
    completed_outcomes = [o for o in outcomes if o["outcome"] in ("PASS", "FAIL")]
    
    if not completed_outcomes:
        return {
            "confidence_score": 50,
            "classification": "UNKNOWN",
            "reason": "All runs are pending or incomplete",
            "metrics": {
                "total_runs": len(outcomes),
                "passes": 0,
                "failures": 0,
                "pass_rate": 0,
                "consecutive_passes": 0,
                "consecutive_failures": 0,
                "flaky_transitions": 0
            }
        }
    
    total_runs = len(completed_outcomes)
    passes = sum(1 for o in completed_outcomes if o["outcome"] == "PASS")
    failures = sum(1 for o in completed_outcomes if o["outcome"] == "FAIL")
    pass_rate = (passes / total_runs) * 100 if total_runs > 0 else 0
    
    # Detect flakiness (alternating pass/fail patterns)
    is_flaky, flaky_transitions = _detect_flakiness(completed_outcomes)
    
    # Calculate consecutive passes at the end (recent stability)
    consecutive_passes = _count_consecutive_passes(completed_outcomes)
    
    # Calculate consecutive failures at the end (recent instability)
    consecutive_failures = _count_consecutive_failures(completed_outcomes)
    
    metrics = {
        "total_runs": total_runs,
        "passes": passes,
        "failures": failures,
        "pass_rate": round(pass_rate, 1),
        "consecutive_passes": consecutive_passes,
        "consecutive_failures": consecutive_failures,
        "flaky_transitions": flaky_transitions
    }
    
    # --- Classification Logic (Deterministic & Explainable) ---
    
    # RELIABLE: No failures in substantial history
    if total_runs >= 10 and failures == 0:
        return {
            "confidence_score": 100,
            "classification": "RELIABLE",
            "reason": f"Perfect track record: {total_runs} consecutive passes with no failures",
            "metrics": metrics
        }
    
    # RELIABLE: Very high pass rate with sufficient history (even with 1 failure at end)
    if total_runs >= 15 and pass_rate >= 93:
        score = 90 + min(10, int((pass_rate - 90)))  # 90-100
        return {
            "confidence_score": int(score),
            "classification": "RELIABLE",
            "reason": f"Highly stable: {pass_rate:.1f}% pass rate over {total_runs} runs ({failures} failure{'s' if failures > 1 else ''})",
            "metrics": metrics
        }
    
    # STABLE: Recent consecutive passes with good history (Check BEFORE flakiness)
    if consecutive_passes >= 5 and pass_rate >= 70:
        score = 70 + min(15, consecutive_passes * 2)  # 70-85
        return {
            "confidence_score": int(score),
            "classification": "STABLE",
            "reason": f"Recently stable: {consecutive_passes} consecutive passes (overall {pass_rate:.1f}% pass rate)",
            "metrics": metrics
        }
    
    # STABLE: Moderate consecutive passes (Check BEFORE flakiness)
    if consecutive_passes >= 3 and pass_rate >= 60 and not is_flaky:
        score = 70 + (consecutive_passes * 3)  # 79-85 range
        return {
            "confidence_score": min(85, int(score)),
            "classification": "STABLE",
            "reason": f"Stabilizing: {consecutive_passes} recent passes out of {total_runs} total runs",
            "metrics": metrics
        }
    
    # FLAKY: Alternating pass/fail patterns detected
    if is_flaky:
        # Score based on pass rate but cap at 50
        score = max(20, min(50, int(pass_rate / 2)))
        return {
            "confidence_score": score,
            "classification": "FLAKY",
            "reason": f"Inconsistent behavior: {flaky_transitions} pass/fail transitions detected across {total_runs} runs",
            "metrics": metrics
        }
    
    # UNSTABLE: Consistent failures
    if consecutive_failures >= 3:
        score = max(10, 30 - (consecutive_failures * 3))  # Lower score for more failures
        return {
            "confidence_score": int(score),
            "classification": "UNSTABLE",
            "reason": f"Failing consistently: {consecutive_failures} consecutive failures",
            "metrics": metrics
        }
    
    # UNSTABLE: All runs failed
    if failures == total_runs and total_runs >= 3:
        return {
            "confidence_score": 10,
            "classification": "UNSTABLE",
            "reason": f"Complete failure: All {total_runs} runs failed",
            "metrics": metrics
        }
    
    # UNSTABLE: Poor pass rate
    if pass_rate < 50 and total_runs >= 5:
        score = max(15, int(pass_rate / 2))  # 15-25 range
        return {
            "confidence_score": score,
            "classification": "UNSTABLE",
            "reason": f"Low reliability: {pass_rate:.1f}% pass rate ({passes}/{total_runs} runs)",
            "metrics": metrics
        }
    
    # UNKNOWN: Insufficient data
    if total_runs < 3:
        score = 40 + (total_runs * 5)  # 45-50 range
        return {
            "confidence_score": score,
            "classification": "UNKNOWN",
            "reason": f"Insufficient data: Only {total_runs} run(s) available",
            "metrics": metrics
        }
    
    # DEFAULT: Moderate pass rate, no clear pattern
    score = int(pass_rate * 0.7)  # Scale down to 0-70 range
    if pass_rate >= 60:
        classification = "STABLE"
        reason = f"Moderate stability: {pass_rate:.1f}% pass rate over {total_runs} runs"
    else:
        classification = "UNSTABLE"
        reason = f"Unreliable: {pass_rate:.1f}% pass rate ({passes}/{total_runs} runs passed)"
    
    return {
        "confidence_score": max(30, min(70, score)),
        "classification": classification,
        "reason": reason,
        "metrics": metrics
    }


def _detect_flakiness(outcomes):
    """
    Detect if a check is flaky based on alternating pass/fail patterns
    
    Returns:
        (is_flaky: bool, transition_count: int)
    """
    if len(outcomes) < 4:
        return False, 0
    
    # Count transitions from PASS to FAIL or FAIL to PASS
    transitions = 0
    for i in range(1, len(outcomes)):
        prev = outcomes[i-1]["outcome"]
        curr = outcomes[i]["outcome"]
        
        if prev in ("PASS", "FAIL") and curr in ("PASS", "FAIL") and prev != curr:
            transitions += 1
    
    # Flaky if we have multiple transitions AND high transition rate
    # At least 3 transitions AND 40%+ of runs are transitions (more strict)
    transition_rate = transitions / len(outcomes) if len(outcomes) > 0 else 0
    is_flaky = transitions >= 3 and transition_rate >= 0.35
    
    return is_flaky, transitions


def _count_consecutive_passes(outcomes):
    """Count consecutive passes at the end of the history"""
    count = 0
    for outcome in reversed(outcomes):
        if outcome["outcome"] == "PASS":
            count += 1
        else:
            break
    return count


def _count_consecutive_failures(outcomes):
    """Count consecutive failures at the end of the history"""
    count = 0
    for outcome in reversed(outcomes):
        if outcome["outcome"] == "FAIL":
            count += 1
        else:
            break
    return count


def generate_confidence_report(check_history):
    """
    Generate a confidence report for all checks in a PR
    
    Args:
        check_history: Dict mapping check names to list of outcomes
    
    Returns:
        Dict with per-check confidence scores and classifications
    """
    report = {}
    
    for check_name, outcomes in check_history.items():
        confidence_data = calculate_confidence_score(outcomes)
        
        current_status = outcomes[-1]["outcome"] if outcomes else "UNKNOWN"
        
        report[check_name] = {
            "check_name": check_name,
            "current_status": current_status,
            "confidence_score": confidence_data["confidence_score"],
            "classification": confidence_data["classification"],
            "reason": confidence_data["reason"],
            "metrics": confidence_data["metrics"]
        }
    
    return report
