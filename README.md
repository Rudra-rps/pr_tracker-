# PR Readiness Demo

Day 1-2 prototype for BLT GSoC Project E.

## What this demo does
- Accepts a GitHub Pull Request URL
- Fetches PR metadata using GitHub REST API
- Retrieves CI status from Check Runs and Commit Statuses
- Aggregates CI signals into a unified state
- Validates input and handles API errors

## What this demo does NOT do
- No review comment/thread analysis (Day 3)
- No readiness classification yet (Day 4)
- No advanced UX or dashboard

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PR_tracker/pr-readiness-demo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up GitHub token**
   
   Create a `.env` file in the `pr-readiness-demo` directory:
   ```
   GITHUB_TOKEN=your_github_personal_access_token
   ```
   
   Get a token from: https://github.com/settings/tokens
   - Requires `public_repo` scope for public PRs

## Usage

```bash
python src/cli.py <github_pr_url>
```

**Example:**
```bash
python src/cli.py https://github.com/zulip/zulip/pull/37753
```

**Output:**
```
PR METADATA
-----------
Title: message_edit: Show message edit button while saving changes.
Author: Pritesh-30
State: open
Commits: 1
Changed files: 5

CI STATUS
---------
Unified CI State: PASS
Signals found: 12
```

## Requirements

- Python 3.7+
- GitHub Personal Access Token
- Dependencies: `requests`, `python-dotenv`

## Why this exists
This prototype demonstrates early integration with GitHub APIs and forms the ingestion layer for a full PR readiness pipeline.
