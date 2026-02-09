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
- ✅ **Confidence scoring engine** (Day 4)
- ✅ **Advanced confidence metrics with explanations** (Day 4)
- ✅ **Enhanced CLI with help, examples, and version commands** (Day 5) ⭐ NEW
- ✅ **Professional output formatting with emojis** (Day 5) ⭐ NEW
- ✅ **Comprehensive error handling and user feedback** (Day 5) ⭐ NEW
- ✅ Validates input and handles API errors

## What this demo does NOT do (yet)
- No dashboard or web UI
- No machine learning or LLMs
- No private repository support
- No time-series visualizations

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
python src/cli.py --help
python src/cli.py --examples
python src/cli.py --version
```

**Examples:**
```bash
# Analyze a PR
python src/cli.py https://github.com/zulip/zulip/pull/37753

# Show help
python src/cli.py --help

# Show usage examples
python src/cli.py --examples

# Show version
python src/cli.py --version
```

**Output:**
```
PR METADATA
-----------
Title: Add user authentication feature
Author: developer123
State: open
Commits: 8
Changed files: 12

CI STATUS
---------
Unified CI State: PASS
Signals found: 5

============================================================
CI RELIABILITY & CONFIDENCE ANALYSIS
============================================================
Analyzing historical CI patterns with confidence scoring...

✅ Check: pytest-unit-tests
   Current Status: PASS
   Confidence Score: 100/100
   Classification: RELIABLE
   History: 15 runs (15 pass, 0 fail, 100.0% pass rate)
   Recent Trend: 15 consecutive passes
   Analysis: Perfect track record: 15 consecutive passes with no failures

🟢 Check: eslint-code-quality
   Current Status: PASS
   Confidence Score: 80/100
   Classification: STABLE
   History: 12 runs (10 pass, 2 fail, 83.3% pass rate)
   Recent Trend: 5 consecutive passes
   Analysis: Recently stable: 5 consecutive passes (overall 83.3% pass rate)

⚠️  Check: integration-tests
   Current Status: PASS
   Confidence Score: 35/100
   Classification: FLAKY
   History: 10 runs (6 pass, 4 fail, 60.0% pass rate)
   Analysis: Inconsistent behavior: 5 pass/fail transitions detected

------------------------------------------------------------
SUMMARY
------------------------------------------------------------
Total Checks: 3
  ✅ Reliable: 1
  🟢 Stable: 1
  ⚠️  Flaky: 1
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
**Phase 4:** CI confidence scoring engine ✅ (Day 4)  
**Phase 5:** Enhanced CLI output & UX ✅ (Day 4)  
**Phase 6:** Edge-case hardening (Day 5)  
**Phase 7:** Dashboard and advisory insights (Day 6-7)

## Day 4 Achievements ⭐ NEW

See [DAY4_QUICKSTART.md](pr-readiness-demo/DAY4_QUICKSTART.md) for complete details.

**Key Features:**
- **Deterministic Confidence Scoring**: 0-100 score for every CI check
- **Priority-based Classification**: RELIABLE (90-100), STABLE (70-89), FLAKY (20-50), UNSTABLE (10-30), UNKNOWN (40-60)
- **Advanced Flakiness Detection**: 35%+ transition rate threshold with 3+ transitions
- **Recent Trend Analysis**: Consecutive passes/failures weighted heavily
- **Transparent Explanations**: Every score includes detailed reasoning
- **Enhanced CLI Visualization**: Visual indicators (✅🟢⚠️❌❔) and summary statistics
- **Comprehensive Testing**: 13+ scenarios validated with 85%+ accuracy

**Scoring Algorithm Priorities:**
1. ✅ RELIABLE: Perfect track record (10+ runs, 0 failures) or 93%+ pass rate
2. 🟢 STABLE: Recent consecutive passes (3-5+) with good overall rate
3. ⚠️ FLAKY: Alternating pass/fail patterns (35%+ transition rate)
4. ❌ UNSTABLE: Consistent failures or poor pass rate (<50%)
5. ❔ UNKNOWN: Insufficient data (<3 runs)

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
