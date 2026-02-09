import sys
from parser import parse_pr_url
from github.client import GitHubClient
from github.ci import aggregate_ci
from github.history import analyze_ci_reliability

VERSION = "0.1.0"

def print_help():
    """Display comprehensive help information"""
    print("="*70)
    print("CI RELIABILITY & FLAKINESS ANALYTICS")
    print(f"Version {VERSION}")
    print("="*70)
    print()
    print("DESCRIPTION")
    print("  Analyzes GitHub Pull Requests for CI reliability, flakiness detection,")
    print("  and confidence scoring based on historical CI patterns.")
    print()
    print("USAGE")
    print("  python cli.py <github_pr_url>")
    print("  python cli.py --help")
    print("  python cli.py --examples")
    print()
    print("ARGUMENTS")
    print("  <github_pr_url>    Full GitHub Pull Request URL")
    print("                     Format: https://github.com/owner/repo/pull/number")
    print()
    print("OPTIONS")
    print("  -h, --help         Show this help message")
    print("  -e, --examples     Show usage examples")
    print("  -v, --version      Show version information")
    print()
    print("SETUP")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Set GITHUB_TOKEN in .env file")
    print("  3. Get token from: https://github.com/settings/tokens")
    print()
    print("OUTPUT")
    print("  • PR metadata (title, author, commits, files)")
    print("  • Unified CI status aggregation")
    print("  • Per-check confidence scores (0-100)")
    print("  • Flakiness detection and stability classification")
    print("  • Historical pattern analysis with explanations")
    print()
    print("For more information, visit: https://github.com/yourusername/PR_tracker")
    print("="*70)

def print_examples():
    """Display usage examples"""
    print("="*70)
    print("USAGE EXAMPLES")
    print("="*70)
    print()
    print("1. Analyze a Zulip PR:")
    print("   $ python cli.py https://github.com/zulip/zulip/pull/37753")
    print()
    print("2. Analyze a Django PR:")
    print("   $ python cli.py https://github.com/django/django/pull/18234")
    print()
    print("3. Analyze a React PR:")
    print("   $ python cli.py https://github.com/facebook/react/pull/28950")
    print()
    print("4. Show help:")
    print("   $ python cli.py --help")
    print()
    print("EXAMPLE OUTPUT")
    print("-" * 70)
    print("✅ Check: pytest-unit-tests")
    print("   Current Status: PASS")
    print("   Confidence Score: 100/100")
    print("   Classification: RELIABLE")
    print("   History: 15 runs (15 pass, 0 fail, 100.0% pass rate)")
    print("   Recent Trend: 15 consecutive passes")
    print("   Analysis: Perfect track record with no failures")
    print()
    print("⚠️  Check: integration-tests")
    print("   Current Status: PASS")
    print("   Confidence Score: 35/100")
    print("   Classification: FLAKY")
    print("   History: 10 runs (6 pass, 4 fail, 60.0% pass rate)")
    print("   Analysis: Inconsistent behavior detected")
    print("-" * 70)
    print()
    print("For more examples, visit: https://github.com/yourusername/PR_tracker")
    print("="*70)

def print_version():
    """Display version information"""
    print(f"CI Reliability Analytics v{VERSION}")
    print("Pre-GSoC feasibility prototype for BLT GSoC 2026")

def main():
    if len(sys.argv) != 2:
        print("Error: Invalid arguments")
        print()
        print("Usage: python cli.py <github_pr_url>")
        print("       python cli.py --help")
        print()
        print("Try 'python cli.py --help' for more information.")
        sys.exit(1)

    pr_url = sys.argv[1]
    
    # Handle help/info commands
    if pr_url in ['-h', '--help']:
        print_help()
        sys.exit(0)
    
    if pr_url in ['-e', '--examples']:
        print_examples()
        sys.exit(0)
    
    if pr_url in ['-v', '--version']:
        print_version()
        sys.exit(0)

    # Print header
    print()
    print("="*70)
    print("CI RELIABILITY & FLAKINESS ANALYTICS v" + VERSION)
    print("="*70)
    print()
    
    try:
        print(f"📥 Analyzing PR: {pr_url}")
        print()
        
        pr_info = parse_pr_url(pr_url)
        
        print("🔍 Fetching PR metadata...")
        client = GitHubClient()
        pr = client.get_pull_request(
            pr_info["owner"],
            pr_info["repo"],
            pr_info["number"]
        )

        print()
        print("="*70)
        print("PR METADATA")
        print("="*70)
        print(f"Repository:    {pr_info['owner']}/{pr_info['repo']}")
        print(f"PR Number:     #{pr_info['number']}")
        print(f"Title:         {pr['title']}")
        print(f"Author:        {pr['user']['login']}")
        print(f"State:         {pr['state'].upper()}")
        print(f"Commits:       {pr['commits']}")
        print(f"Changed Files: {pr['changed_files']}")
        
        print()
        print("🔍 Fetching CI status...")
        
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

        print()
        print("="*70)
        print("CI STATUS")
        print("="*70)
        
        # Add visual indicator for CI state
        ci_emoji = {
            "PASS": "✅",
            "FAIL": "❌",
            "PENDING": "⏳",
            "NO_CI": "⚪"
        }
        state_emoji = ci_emoji.get(ci_state, "•")
        
        print(f"Unified CI State: {state_emoji} {ci_state}")
        print(f"CI Checks Found:  {len(ci_details)}")

        # Day 3: Historical CI Pattern Analysis
        # Day 4: CI Confidence Scoring Engine
        # Day 5: Enhanced CLI Output & UX
        print()
        print("🔍 Analyzing historical CI patterns...")
        print()
        print("="*70)
        print("CI RELIABILITY & CONFIDENCE ANALYSIS")
        print("="*70)
        print()
        
        reliability_report = analyze_ci_reliability(
            client,
            pr_info["owner"],
            pr_info["repo"],
            pr_info["number"]
        )

        if not reliability_report:
            print("⚠️  No CI history data available for analysis")
            print("    This PR may not have enough commits with CI runs yet.")
        else:
            # Sort checks by confidence score (descending)
            sorted_checks = sorted(
                reliability_report.items(),
                key=lambda x: x[1]['confidence_score'],
                reverse=True
            )
            
            for check_name, report in sorted_checks:
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
                      f"{metrics['pass_rate']:.1f}% pass rate)")
                
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
            
            print("="*70)
            print("SUMMARY")
            print("="*70)
            print(f"Total Checks Analyzed: {len(reliability_report)}")
            print()
            if reliable_count > 0:
                print(f"  ✅ Reliable: {reliable_count} check(s)")
            if stable_count > 0:
                print(f"  🟢 Stable:   {stable_count} check(s)")
            if flaky_count > 0:
                print(f"  ⚠️  Flaky:    {flaky_count} check(s)")
            if unstable_count > 0:
                print(f"  ❌ Unstable: {unstable_count} check(s)")
            if unknown_count > 0:
                print(f"  ❔ Unknown:  {unknown_count} check(s)")
            
            # Overall verdict with recommendations
            print()
            print("="*70)
            if flaky_count > 0 or unstable_count > 0:
                print("⚠️  WARNING: Some CI checks show reliability concerns")
                if flaky_count > 0:
                    print("    → Investigate flaky checks for intermittent failures")
                if unstable_count > 0:
                    print("    → Review unstable checks for consistent failures")
            elif unknown_count == len(reliability_report):
                print("ℹ️  INFO: Insufficient CI history for confidence analysis")
                print("    → More commits needed to establish reliability patterns")
            else:
                print("✅ GOOD: All CI checks show good reliability")
                print("    → Safe to trust these CI signals for merge decisions")
            print("="*70)
            print()
        
        print("✨ Analysis complete!")
        print()

    except ValueError as e:
        print()
        print("="*70)
        print("❌ ERROR: Invalid Input")
        print("="*70)
        print(f"   {str(e)}")
        print()
        print("Expected format: https://github.com/owner/repo/pull/number")
        print("Example:         https://github.com/zulip/zulip/pull/37753")
        print()
        print("Try 'python cli.py --help' for more information.")
        print("="*70)
        sys.exit(1)
    except PermissionError as e:
        print()
        print("="*70)
        print("❌ ERROR: Authentication Failed")
        print("="*70)
        print(f"   {str(e)}")
        print()
        print("Please ensure:")
        print("  1. GITHUB_TOKEN is set in .env file")
        print("  2. Token has 'public_repo' scope")
        print("  3. Token is valid and not expired")
        print()
        print("Get a token from: https://github.com/settings/tokens")
        print("="*70)
        sys.exit(1)
    except ConnectionError as e:
        print()
        print("="*70)
        print("❌ ERROR: Network Connection Failed")
        print("="*70)
        print(f"   {str(e)}")
        print()
        print("Please check:")
        print("  1. Your internet connection")
        print("  2. GitHub API status: https://www.githubstatus.com/")
        print("  3. Firewall or proxy settings")
        print("="*70)
        sys.exit(1)
    except KeyError as e:
        print()
        print("="*70)
        print("❌ ERROR: Data Access Failed")
        print("="*70)
        print(f"   Missing expected data: {str(e)}")
        print()
        print("This may indicate:")
        print("  1. The PR may have been deleted or moved")
        print("  2. The repository structure changed")
        print("  3. API response format changed")
        print("="*70)
        sys.exit(1)
    except Exception as e:
        print()
        print("="*70)
        print("❌ ERROR: Unexpected Error Occurred")
        print("="*70)
        print(f"   {type(e).__name__}: {str(e)}")
        print()
        print("Please try:")
        print("  1. Verify the PR URL is correct")
        print("  2. Check if the repository is public")
        print("  3. Try again in a few moments")
        print()
        print("If the issue persists, please report it with the error details above.")
        print("="*70)
        sys.exit(1)

if __name__ == "__main__":
    main()
