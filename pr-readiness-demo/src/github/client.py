import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_API = "https://api.github.com"

class GitHubClient:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise PermissionError("GITHUB_TOKEN not set in .env file")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        })
    
    def _handle_rate_limit(self, response):
        """Check and handle rate limit responses"""
        if response.status_code == 403:
            # Check if it's rate limit or access denied
            remaining = response.headers.get('X-RateLimit-Remaining', '0')
            if remaining == '0':
                reset_time = response.headers.get('X-RateLimit-Reset', 'unknown')
                raise ConnectionError(
                    f"GitHub API rate limit exceeded. Resets at Unix timestamp: {reset_time}. "
                    "Consider using an authenticated token or waiting before retrying."
                )
            else:
                raise PermissionError("Access denied. Check your token permissions or if the repository is private.")
        
    def _check_response(self, response, error_context="GitHub API request"):
        """Centralized response checking with detailed error messages"""
        if response.status_code == 404:
            raise ValueError(f"{error_context} failed: Resource not found (404). Check if PR/repository exists and is public.")
        
        self._handle_rate_limit(response)
        
        if response.status_code >= 500:
            raise ConnectionError(f"{error_context} failed: GitHub server error ({response.status_code}). Try again later.")
        
        if not response.ok:
            raise RuntimeError(f"{error_context} failed with status {response.status_code}: {response.text[:200]}")

    def get_pull_request(self, owner: str, repo: str, number: str):
        url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{number}"
        try:
            r = self.session.get(url, timeout=10)
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out. Check your internet connection.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Network connection failed. Check your internet connection.")
        
        self._check_response(r, f"Fetching PR #{number}")
        return r.json()

    def get_pr_head_sha(self, owner, repo, number):
        pr = self.get_pull_request(owner, repo, number)
        return pr["head"]["sha"]
    
    def get_check_runs(self, owner, repo, sha):
        url = f"{GITHUB_API}/repos/{owner}/{repo}/commits/{sha}/check-runs"
        try:
            r = self.session.get(url, timeout=10)
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out while fetching check runs.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Network connection failed while fetching check runs.")
        
        self._check_response(r, "Fetching check runs")
        return r.json().get("check_runs", [])
    
    def get_commit_statuses(self, owner, repo, sha):
        url = f"{GITHUB_API}/repos/{owner}/{repo}/commits/{sha}/statuses"
        try:
            r = self.session.get(url, timeout=10)
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out while fetching commit statuses.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Network connection failed while fetching commit statuses.")
        
        self._check_response(r, "Fetching commit statuses")
        return r.json()
    
    def get_pr_commits(self, owner, repo, number):
        """Fetch all commits from the PR"""
        url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{number}/commits"
        try:
            r = self.session.get(url, timeout=10)
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out while fetching PR commits.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Network connection failed while fetching PR commits.")
        
        self._check_response(r, "Fetching PR commits")
        return r.json()

    
    