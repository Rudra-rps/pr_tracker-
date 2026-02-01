def aggregate_ci(check_runs, statuses):
    if not check_runs and not statuses:
        return "NO_CI", []

    results = []

    for c in check_runs:
        results.append({
            "name": c["name"],
            "status": c["status"],
            "conclusion": c["conclusion"]
        })

    for s in statuses:
        results.append({
            "name": s["context"],
            "status": s["state"],
            "conclusion": s["state"]
        })

    for r in results:
        if r["conclusion"] in ("failure", "cancelled", "timed_out", "error"):
            return "FAIL", results

    for r in results:
        if r["status"] in ("queued", "in_progress", "pending"):
            return "PENDING", results

    return "PASS", results
