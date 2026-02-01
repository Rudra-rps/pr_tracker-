import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_API = "https://api.github.com"

class GitHubClient:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise RuntimeError("GITHUB_TOKEN not set")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        })

    def get_pull_request(self, owner: str, repo: str, number: str):
        url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{number}"
        r = self.session.get(url)

        if r.status_code == 404:
            raise ValueError("PR not found or repository is private")
        if r.status_code == 403:
            raise RuntimeError("Rate limit exceeded or access denied")
        if not r.ok:
            raise RuntimeError(f"GitHub API error: {r.status_code}")

        return r.json()

    def get_pr_head_sha(self, owner, repo, number):
       pr = self.get_pull_request(owner, repo, number)
       return pr["head"]["sha"]
    
    def get_check_runs(self, owner, repo, sha):
        url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}/check-runs"
        r = self.session.get(url)

        if not r.ok:
            raise RuntimeError("Failed to fetch check runs")
        
        return r.json().get("check_runs", [])
    
    def get_commit_statuses(self, owner, repo, sha):
        url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}/statuses"
        r = self.session.get(url)

        if not r.ok:
            raise RuntimeError("Failed to fetch commit statuses")
        
        return r.json()
    

    
    