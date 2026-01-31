import sys
from parser import parse_pr_url
from github.client import GitHubClient

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

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
