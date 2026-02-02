# CI Reliability & Flakiness Analytics

**Pre-GSoC feasibility prototype for BLT GSoC 2026**

## Project Positioning

This project complements Project E (PR Readiness Dashboard) by analyzing **CI signal reliability** — helping maintainers understand which CI checks are trustworthy vs flaky, without overlapping the core review-state readiness pipeline.

**Focus:** CI confidence scoring, flakiness detection, and stability pattern analysis.

## What this demo does
- ✅ Accepts a GitHub Pull Request URL
- ✅ Fetches PR metadata using GitHub REST API
- ✅ Retrieves CI status from Check Runs and Commit Statuses
- ✅ Aggregates CI signals into a unified state
- ✅ **Historical CI pattern analysis** (Day 3)
- ✅ **Flaky check detection** (Day 3)
- ✅ **Stability classification** (Day 3)
- ✅ **Confidence scoring per check** (Day 3)
- ✅ Validates input and handles API errors

## What this demo does NOT do (yet)
- No JSON output format (Day 4)
- No advanced confidence scoring (Day 4)
- No stability pattern visualization
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

CI RELIABILITY ANALYSIS
-----------------------
Analyzing historical CI patterns...

Check: pytest
  Current Status: PASS
  Classification: STABLE
  Stability Score: 85/100
  History: 6 runs (5 pass, 1 fail)
  Analysis: 4 consecutive passes detected

Check: lint
  Current Status: PASS
  Classification: RELIABLE
  Stability Score: 100/100
  History: 12 runs (12 pass, 0 fail)
  Analysis: No failures in 12 consecutive runs
```

## Requirements

- Python 3.7+
- GitHub Personal Access Token
- Dependencies: `requests`, `python-dotenv`

## Why this exists

This prototype demonstrates:
- Early integration with GitHub CI APIs (Check Runs, Commit Statuses)
- Foundation for CI reliability analysis
- Deterministic, explainable approach to CI signal processing

**Problem it solves:** Maintainers often struggle to determine if a failing CI check is a real issue or just a flaky test. This project aims to surface CI reliability patterns to inform merge decisions.

## Roadmap to Full Project

**Phase 1:** CI data ingestion and aggregation ✅ (Day 1-2)  
**Phase 2:** Historical CI pattern analysis ✅ (Day 3)  
**Phase 3:** Flaky check detection algorithm ✅ (Day 3)  
**Phase 4:** CI confidence scoring per workflow ✅ (Day 3)  
**Phase 5:** Enhanced scoring engine (Day 4)  
**Phase 6:** Dashboard and advisory insights (Day 5)

## Day 3 Achievements

See [DAY3_QUICKSTART.md](pr-readiness-demo/DAY3_QUICKSTART.md) for details.

**Key Features:**
- Historical CI tracking across all PR commits
- Flakiness detection (alternating pass/fail patterns)
- Stability classification: RELIABLE, STABLE, FLAKY, UNSTABLE, UNKNOWN
- Confidence scoring (0-100) with transparent explanations
- Deterministic heuristics (no ML/NLP)
- Comprehensive test suite

**Heuristics Implemented:**
- ✅ Same check, different outcomes → FLAKY
- ✅ 3+ consecutive passes → STABLE
- ✅ No failures in 10+ runs → RELIABLE (100% confidence)
- ✅ All deterministic, explainable logic
