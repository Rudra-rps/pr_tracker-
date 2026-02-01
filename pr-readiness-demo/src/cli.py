import sys
from parser import parse_pr_url
from github.client import GitHubClient
from github.ci import aggregate_ci

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

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
