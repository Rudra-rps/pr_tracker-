"""
Historical CI Pattern Analysis Module
Tracks CI check outcomes across commits to detect flakiness and stability patterns
"""

from .confidence import generate_confidence_report

def normalize_ci_outcome(check_run=None, status=None):
    """
    Normalize a CI check result into PASS, FAIL, or PENDING
    """
    if check_run:
        conclusion = check_run.get("conclusion")
        if conclusion in ("success",):
            return "PASS"
        elif conclusion in ("failure", "cancelled", "timed_out", "error"):
            return "FAIL"
        else:
            return "PENDING"
    
    if status:
        state = status.get("state")
        if state == "success":
            return "PASS"
        elif state in ("failure", "error"):
            return "FAIL"
        else:
            return "PENDING"
    
    return "UNKNOWN"


def build_ci_history(client, owner, repo, pr_number, max_commits=20):
    """
    Build historical CI data for all commits in a PR
    
    Returns:
        Dict mapping check names to list of outcomes across commits
    """
    commits = client.get_pr_commits(owner, repo, pr_number)
    
    # Limit to most recent commits to avoid excessive API calls
    commits = commits[-max_commits:] if len(commits) > max_commits else commits
    
    check_history = {}
    
    for commit in commits:
        sha = commit["sha"]
        
        # Fetch CI data for this commit
        try:
            check_runs = client.get_check_runs(owner, repo, sha)
            statuses = client.get_commit_statuses(owner, repo, sha)
        except Exception:
            # Skip commits with API errors
            continue
        
        # Process check runs
        for check in check_runs:
            name = check["name"]
            outcome = normalize_ci_outcome(check_run=check)
            
            if name not in check_history:
                check_history[name] = []
            
            check_history[name].append({
                "sha": sha,
                "outcome": outcome,
                "commit_date": commit.get("commit", {}).get("committer", {}).get("date", "")
            })
        
        # Process commit statuses
        for status in statuses:
            name = status["context"]
            outcome = normalize_ci_outcome(status=status)
            
            if name not in check_history:
                check_history[name] = []
            
            check_history[name].append({
                "sha": sha,
                "outcome": outcome,
                "commit_date": commit.get("commit", {}).get("committer", {}).get("date", "")
            })
    
    return check_history


def detect_flakiness(outcomes):
    """
    Detect if a check is flaky based on outcome patterns
    
    Heuristic: Same check name with alternating pass/fail outcomes
    
    Returns True if flaky, False otherwise
    """
    if len(outcomes) < 2:
        return False
    
    # Count transitions from PASS to FAIL or FAIL to PASS
    transitions = 0
    for i in range(1, len(outcomes)):
        prev = outcomes[i-1]["outcome"]
        curr = outcomes[i]["outcome"]
        
        if prev in ("PASS", "FAIL") and curr in ("PASS", "FAIL") and prev != curr:
            transitions += 1
    
    # If we have alternating outcomes, it's flaky
    return transitions >= 2


def calculate_stability_metrics(outcomes):
    """
    Calculate stability metrics for a check
    
    Heuristics:
    - 3+ consecutive passes → stable
    - No failures in 10+ runs → high confidence
    - Alternating outcomes → flaky
    
    Returns:
        dict with stability_score, classification, and explanation
    """
    if not outcomes:
        return {
            "stability_score": 0,
            "classification": "UNKNOWN",
            "explanation": "No historical data available"
        }
    
    # Filter out PENDING status for analysis
    completed_outcomes = [o for o in outcomes if o["outcome"] in ("PASS", "FAIL")]
    
    if not completed_outcomes:
        return {
            "stability_score": 0,
            "classification": "UNKNOWN",
            "explanation": "No completed runs found"
        }
    
    total_runs = len(completed_outcomes)
    passes = sum(1 for o in completed_outcomes if o["outcome"] == "PASS")
    failures = sum(1 for o in completed_outcomes if o["outcome"] == "FAIL")
    
    # Check for flakiness
    is_flaky = detect_flakiness(completed_outcomes)
    
    # Calculate consecutive passes at the end
    consecutive_passes = 0
    for outcome in reversed(completed_outcomes):
        if outcome["outcome"] == "PASS":
            consecutive_passes += 1
        else:
            break
    
    # Determine classification and score
    if is_flaky:
        classification = "FLAKY"
        stability_score = max(20, min(50, int((passes / total_runs) * 100)))
        explanation = f"Alternating pass/fail detected across {total_runs} runs"
    
    elif total_runs >= 10 and failures == 0:
        classification = "RELIABLE"
        stability_score = 100
        explanation = f"No failures in {total_runs} consecutive runs"
    
    elif consecutive_passes >= 3:
        classification = "STABLE"
        stability_score = min(95, 70 + (consecutive_passes * 5))
        explanation = f"{consecutive_passes} consecutive passes detected"
    
    elif failures == total_runs:
        classification = "UNSTABLE"
        stability_score = 10
        explanation = f"Failed all {total_runs} runs"
    
    elif total_runs < 5:
        classification = "UNKNOWN"
        stability_score = 50
        explanation = f"Insufficient data ({total_runs} runs)"
    
    else:
        classification = "UNSTABLE"
        pass_rate = int((passes / total_runs) * 100)
        stability_score = pass_rate
        explanation = f"Pass rate: {pass_rate}% ({passes}/{total_runs} runs)"
    
    return {
        "stability_score": stability_score,
        "classification": classification,
        "explanation": explanation,
        "total_runs": total_runs,
        "passes": passes,
        "failures": failures
    }


def analyze_ci_reliability(client, owner, repo, pr_number):
    """
    Main function to analyze CI reliability for a PR using the confidence scoring engine
    
    Returns:
        Dict with per-check confidence scores and reliability metrics
    """
    check_history = build_ci_history(client, owner, repo, pr_number)
    
    # Use the Day 4 confidence scoring engine
    reliability_report = generate_confidence_report(check_history)
    
    return reliability_report
