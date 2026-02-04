import sys
from parser import parse_pr_url
from github.client import GitHubClient
from github.ci import aggregate_ci
from github.history import analyze_ci_reliability

def main():
    if len(sys.argv) != 2:
        print("Usage: python cli.py <github_pr_url>")
        sys.exit(1)

    pr_url = sys.argv[1]

    try:
        pr_info = parse_pr_url(pr_url)
        client = GitHubClient()
        pr = client.get_pull_request(
            pr_info["owner"],
            pr_info["repo"],
            pr_info["number"]
        )

        print("\nPR METADATA")
        print("-----------")
        print(f"Title: {pr['title']}")
        print(f"Author: {pr['user']['login']}")
        print(f"State: {pr['state']}")
        print(f"Commits: {pr['commits']}")
        print(f"Changed files: {pr['changed_files']}")

        sha = client.get_pr_head_sha(
            pr_info["owner"],
            pr_info["repo"],
            pr_info["number"]
        )

        check_runs = client.get_check_runs(
            pr_info["owner"],
            pr_info["repo"],
            sha
        )

        statuses = client.get_commit_statuses(
            pr_info["owner"],
            pr_info["repo"],
            sha
        )

        ci_state, ci_details = aggregate_ci(check_runs, statuses)

        print("\nCI STATUS")
        print("---------")
        print(f"Unified CI State: {ci_state}")
        print(f"Signals found: {len(ci_details)}")

        # Day 3: Historical CI Pattern Analysis
        # Day 4: CI Confidence Scoring Engine
        print("\n" + "="*60)
        print("CI RELIABILITY & CONFIDENCE ANALYSIS")
        print("="*60)
        print("Analyzing historical CI patterns with confidence scoring...\n")
        
        reliability_report = analyze_ci_reliability(
            client,
            pr_info["owner"],
            pr_info["repo"],
            pr_info["number"]
        )

        if not reliability_report:
            print("⚠️  No CI history data available")
        else:
            for check_name, report in reliability_report.items():
                # Classification emoji
                classification_emoji = {
                    "RELIABLE": "✅",
                    "STABLE": "🟢",
                    "FLAKY": "⚠️",
                    "UNSTABLE": "❌",
                    "UNKNOWN": "❔"
                }
                
                emoji = classification_emoji.get(report['classification'], "•")
                
                print(f"{emoji} Check: {check_name}")
                print(f"   Current Status: {report['current_status']}")
                print(f"   Confidence Score: {report['confidence_score']}/100")
                print(f"   Classification: {report['classification']}")
                
                # Display detailed metrics
                metrics = report['metrics']
                print(f"   History: {metrics['total_runs']} runs " +
                      f"({metrics['passes']} pass, {metrics['failures']} fail, " +
                      f"{metrics['pass_rate']}% pass rate)")
                
                if metrics['consecutive_passes'] > 0:
                    print(f"   Recent Trend: {metrics['consecutive_passes']} consecutive passes")
                elif metrics['consecutive_failures'] > 0:
                    print(f"   Recent Trend: {metrics['consecutive_failures']} consecutive failures")
                
                print(f"   Analysis: {report['reason']}")
                print()
            
            # Overall summary
            classifications = [r['classification'] for r in reliability_report.values()]
            reliable_count = classifications.count('RELIABLE')
            stable_count = classifications.count('STABLE')
            flaky_count = classifications.count('FLAKY')
            unstable_count = classifications.count('UNSTABLE')
            unknown_count = classifications.count('UNKNOWN')
            
            print("-" * 60)
            print("SUMMARY")
            print("-" * 60)
            print(f"Total Checks: {len(reliability_report)}")
            if reliable_count > 0:
                print(f"  ✅ Reliable: {reliable_count}")
            if stable_count > 0:
                print(f"  🟢 Stable: {stable_count}")
            if flaky_count > 0:
                print(f"  ⚠️  Flaky: {flaky_count}")
            if unstable_count > 0:
                print(f"  ❌ Unstable: {unstable_count}")
            if unknown_count > 0:
                print(f"  ❔ Unknown: {unknown_count}")
            
            # Overall verdict
            print()
            if flaky_count > 0 or unstable_count > 0:
                print("⚠️  WARNING: Some CI checks show reliability concerns")
            elif unknown_count == len(reliability_report):
                print("ℹ️  INFO: Insufficient CI history for confidence analysis")
            else:
                print("✅ GOOD: CI checks show good reliability")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
