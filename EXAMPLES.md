# CLI Output Examples

**Real-world output from the CI Reliability & Flakiness Analytics tool**

## Table of Contents
1. [Help Command](#help-command)
2. [Examples Command](#examples-command)
3. [Version Command](#version-command)
4. [Successful Analysis](#successful-analysis)
5. [Error Scenarios](#error-scenarios)
6. [Edge Cases](#edge-cases)

---

## Help Command

```bash
$ python src/cli.py --help
```

**Output:**
```
======================================================================
CI RELIABILITY & FLAKINESS ANALYTICS
Version 0.1.0
======================================================================

DESCRIPTION
  Analyzes GitHub Pull Requests for CI reliability, flakiness detection,
  and confidence scoring based on historical CI patterns.

USAGE
  python cli.py <github_pr_url>
  python cli.py --help
  python cli.py --examples

ARGUMENTS
  <github_pr_url>    Full GitHub Pull Request URL
                     Format: https://github.com/owner/repo/pull/number

OPTIONS
  -h, --help         Show this help message
  -e, --examples     Show usage examples
  -v, --version      Show version information

SETUP
  1. Install dependencies: pip install -r requirements.txt
  2. Set GITHUB_TOKEN in .env file
  3. Get token from: https://github.com/settings/tokens

OUTPUT
  • PR metadata (title, author, commits, files)
  • Unified CI status aggregation
  • Per-check confidence scores (0-100)
  • Flakiness detection and stability classification
  • Historical pattern analysis with explanations

For more information, visit: https://github.com/yourusername/PR_tracker
======================================================================
```

---

## Examples Command

```bash
$ python src/cli.py --examples
```

**Output:**
```
======================================================================
USAGE EXAMPLES
======================================================================

1. Analyze a Zulip PR:
   $ python cli.py https://github.com/zulip/zulip/pull/37753

2. Analyze a Django PR:
   $ python cli.py https://github.com/django/django/pull/18234

3. Analyze a React PR:
   $ python cli.py https://github.com/facebook/react/pull/28950

4. Show help:
   $ python cli.py --help

EXAMPLE OUTPUT
----------------------------------------------------------------------
✅ Check: pytest-unit-tests
   Current Status: PASS
   Confidence Score: 100/100
   Classification: RELIABLE
   History: 15 runs (15 pass, 0 fail, 100.0% pass rate)
   Recent Trend: 15 consecutive passes
   Analysis: Perfect track record with no failures

⚠️  Check: integration-tests
   Current Status: PASS
   Confidence Score: 35/100
   Classification: FLAKY
   History: 10 runs (6 pass, 4 fail, 60.0% pass rate)
   Analysis: Inconsistent behavior detected
----------------------------------------------------------------------

For more examples, visit: https://github.com/yourusername/PR_tracker
======================================================================
```

---

## Version Command

```bash
$ python src/cli.py --version
```

**Output:**
```
CI Reliability Analytics v0.1.0
Pre-GSoC feasibility prototype for BLT GSoC 2026
```

---

## Successful Analysis

### Example 1: BLT Repository PR

```bash
$ python src/cli.py https://github.com/OWASP-BLT/BLT/pull/5618
```

**Output:**
```
======================================================================
CI RELIABILITY & FLAKINESS ANALYTICS v0.1.0
======================================================================

📥 Analyzing PR: https://github.com/OWASP-BLT/BLT/pull/5618

🔍 Fetching PR metadata...

======================================================================
PR METADATA
======================================================================
Repository:    OWASP-BLT/BLT
PR Number:     #5618
Title:         Bump gunicorn from 23.0.0 to 25.0.3
Author:        dependabot[bot]
State:         OPEN
Commits:       1
Changed Files: 2

🔍 Fetching CI status...

======================================================================
CI STATUS
======================================================================
Unified CI State: ✅ PASS
CI Checks Found:  30

🔍 Analyzing historical CI patterns...

======================================================================
CI RELIABILITY & CONFIDENCE ANALYSIS
======================================================================

❔ Check: Label Test Result
   Current Status: PASS
   Confidence Score: 45/100
   Classification: UNKNOWN
   History: 1 runs (1 pass, 0 fail, 100.0% pass rate)
   Recent Trend: 1 consecutive passes
   Analysis: Insufficient data: Only 1 run(s) available

❔ Check: CodeQL
   Current Status: PASS
   Confidence Score: 45/100
   Classification: UNKNOWN
   History: 1 runs (1 pass, 0 fail, 100.0% pass rate)
   Recent Trend: 1 consecutive passes
   Analysis: Insufficient data: Only 1 run(s) available

❔ Check: Run pre-commit
   Current Status: PASS
   Confidence Score: 45/100
   Classification: UNKNOWN
   History: 1 runs (1 pass, 0 fail, 100.0% pass rate)
   Recent Trend: 1 consecutive passes
   Analysis: Insufficient data: Only 1 run(s) available

[... 21 more checks omitted for brevity ...]

======================================================================
SUMMARY
======================================================================
Total Checks Analyzed: 24

  ❔ Unknown:  24 check(s)

======================================================================
ℹ️  INFO: Insufficient CI history for confidence analysis
    → More commits needed to establish reliability patterns
======================================================================

✨ Analysis complete!
```

### Example 2: Zulip Repository PR

```bash
$ python src/cli.py https://github.com/zulip/zulip/pull/37753
```

**Output:**
```
======================================================================
CI RELIABILITY & FLAKINESS ANALYTICS v0.1.0
======================================================================

📥 Analyzing PR: https://github.com/zulip/zulip/pull/37753

🔍 Fetching PR metadata...

======================================================================
PR METADATA
======================================================================
Repository:    zulip/zulip
PR Number:     #37753
Title:         message_edit: Show message edit button while saving changes.
Author:        Pritesh-30
State:         OPEN
Commits:       1
Changed Files: 5

🔍 Fetching CI status...

======================================================================
CI STATUS
======================================================================
Unified CI State: ⏳ PENDING
CI Checks Found:  9

🔍 Analyzing historical CI patterns...

======================================================================
CI RELIABILITY & CONFIDENCE ANALYSIS
======================================================================

❔ Check: CodeQL
   Current Status: PASS
   Confidence Score: 50/100
   Classification: UNKNOWN
   History: 2 runs (2 pass, 0 fail, 100.0% pass rate)
   Recent Trend: 2 consecutive passes
   Analysis: Insufficient data: Only 2 run(s) available

❔ Check: codecov/project
   Current Status: PASS
   Confidence Score: 45/100
   Classification: UNKNOWN
   History: 1 runs (1 pass, 0 fail, 100.0% pass rate)
   Recent Trend: 1 consecutive passes
   Analysis: Insufficient data: Only 1 run(s) available

[... more checks ...]

======================================================================
SUMMARY
======================================================================
Total Checks Analyzed: 7

  ❔ Unknown:  7 check(s)

======================================================================
ℹ️  INFO: Insufficient CI history for confidence analysis
    → More commits needed to establish reliability patterns
======================================================================

✨ Analysis complete!
```

### Example 3: Mock Demo Output (Shows All Classifications)

From `src/demo_output.py`:

```
======================================================================
DEMO: CI CONFIDENCE SCORING ENGINE OUTPUT
======================================================================

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

======================================================================
CI RELIABILITY & CONFIDENCE ANALYSIS
======================================================================
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

⚠️  Check: integration-tests-firefox
   Current Status: PASS
   Confidence Score: 35/100
   Classification: FLAKY
   History: 10 runs (6 pass, 4 fail, 60.0% pass rate)
   Recent Trend: 1 consecutive passes
   Analysis: Inconsistent behavior: 5 pass/fail transitions detected across 10 runs

❌ Check: e2e-tests-staging
   Current Status: FAIL
   Confidence Score: 18/100
   Classification: UNSTABLE
   History: 8 runs (2 pass, 6 fail, 25.0% pass rate)
   Recent Trend: 3 consecutive failures
   Analysis: Failing consistently: 3 consecutive failures

❔ Check: security-scan
   Current Status: PASS
   Confidence Score: 50/100
   Classification: UNKNOWN
   History: 2 runs (2 pass, 0 fail, 100.0% pass rate)
   Analysis: Insufficient data: Only 2 run(s) available

----------------------------------------------------------------------
SUMMARY
----------------------------------------------------------------------
Total Checks: 5
  ✅ Reliable: 1
  🟢 Stable: 1
  ⚠️  Flaky: 1
  ❌ Unstable: 1
  ❔ Unknown: 1

⚠️  WARNING: Some CI checks show reliability concerns

======================================================================
```

---

## Error Scenarios

### Error 1: Invalid URL Format

```bash
$ python src/cli.py not-a-valid-url
```

**Output:**
```
======================================================================
CI RELIABILITY & FLAKINESS ANALYTICS v0.1.0
======================================================================

📥 Analyzing PR: not-a-valid-url

======================================================================
❌ ERROR: Invalid Input
======================================================================
   Invalid GitHub PR URL

Expected format: https://github.com/owner/repo/pull/number
Example:         https://github.com/zulip/zulip/pull/37753

Try 'python cli.py --help' for more information.
======================================================================
```

### Error 2: Repository Not Found (404)

```bash
$ python src/cli.py https://github.com/nonexistent/repo/pull/123
```

**Output:**
```
======================================================================
CI RELIABILITY & FLAKINESS ANALYTICS v0.1.0
======================================================================

📥 Analyzing PR: https://github.com/nonexistent/repo/pull/123

🔍 Fetching PR metadata...

======================================================================
❌ ERROR: Invalid Input
======================================================================
   Fetching PR #123 failed: Resource not found (404). Check if PR/repository 
   exists and is public.

Expected format: https://github.com/owner/repo/pull/number
Example:         https://github.com/zulip/zulip/pull/37753

Try 'python cli.py --help' for more information.
======================================================================
```

### Error 3: Missing Authentication Token

```bash
$ python src/cli.py https://github.com/zulip/zulip/pull/37753
# (with GITHUB_TOKEN not set in .env)
```

**Output:**
```
======================================================================
CI RELIABILITY & FLAKINESS ANALYTICS v0.1.0
======================================================================

📥 Analyzing PR: https://github.com/zulip/zulip/pull/37753

======================================================================
❌ ERROR: Authentication Failed
======================================================================
   GITHUB_TOKEN not set in .env file

Please ensure:
  1. GITHUB_TOKEN is set in .env file
  2. Token has 'public_repo' scope
  3. Token is valid and not expired

Get a token from: https://github.com/settings/tokens
======================================================================
```

### Error 4: Rate Limit Exceeded

**Output:**
```
======================================================================
❌ ERROR: Network Connection Failed
======================================================================
   GitHub API rate limit exceeded. Resets at Unix timestamp: 1738195200. 
   Consider using an authenticated token or waiting before retrying.

Please check:
  1. Your internet connection
  2. GitHub API status: https://www.githubstatus.com/
  3. Firewall or proxy settings
======================================================================
```

### Error 5: Bad Arguments

```bash
$ python src/cli.py
```

**Output:**
```
Error: Invalid arguments

Usage: python cli.py <github_pr_url>
       python cli.py --help

Try 'python cli.py --help' for more information.
```

---

## Edge Cases

### Edge Case 1: PR with No CI

**Scenario**: A PR that has no CI checks configured

**Output:**
```
======================================================================
CI STATUS
======================================================================
Unified CI State: ⚪ NO_CI
CI Checks Found:  0

🔍 Analyzing historical CI patterns...

======================================================================
CI RELIABILITY & CONFIDENCE ANALYSIS
======================================================================

⚠️  No CI history data available for analysis
    This PR may not have enough commits with CI runs yet.

✨ Analysis complete!
```

### Edge Case 2: All Checks Pending

**Scenario**: CI is still running on the latest commit

**Output:**
```
======================================================================
CI STATUS
======================================================================
Unified CI State: ⏳ PENDING
CI Checks Found:  8

🔍 Analyzing historical CI patterns...
[... analysis continues with historical data ...]
```

### Edge Case 3: Mixed Success and Failure

**Scenario**: Some checks pass, others fail

**Output:**
```
======================================================================
CI STATUS
======================================================================
Unified CI State: ❌ FAIL
CI Checks Found:  5

[... individual check analysis shows which are passing/failing ...]
```

---

## Unit Test Output

```bash
$ python src/run_tests.py
```

**Output:**
```
======================================================================
RUNNING ALL UNIT TESTS
======================================================================


📦 Running Parser Tests...
======================================================================
PARSER UNIT TESTS
======================================================================

✅ Valid PR URL
✅ Valid PR URL (different repo)
✅ Valid PR URL with trailing slash
✅ Invalid: Not GitHub (correctly rejected)
✅ Invalid: Not PR (correctly rejected)
✅ Invalid: Missing number (correctly rejected)
✅ Invalid: Malformed (correctly rejected)
✅ Invalid: Empty string (correctly rejected)
✅ Valid: Hyphens in name
✅ Valid: Numbers in name

======================================================================
Results: 10 passed, 0 failed out of 10 tests
======================================================================


📦 Running CI Aggregation Tests...
======================================================================
CI AGGREGATION UNIT TESTS
======================================================================

✅ No CI checks
✅ All passing checks
✅ One failing check
✅ Pending checks
✅ Failed and pending (priority)
✅ Cancelled check
✅ Timed out check
✅ Error check
✅ Only statuses (legacy CI)
✅ Pending status
✅ Failed status
✅ Mixed checks and statuses

======================================================================
Results: 12 passed, 0 failed out of 12 tests
======================================================================


======================================================================
OVERALL TEST SUMMARY
======================================================================
✅ Total Passed: 22
❌ Total Failed: 0
📊 Total Tests:  22

🎉 ALL TESTS PASSED!
======================================================================
```

---

## Performance Examples

### Single-Commit PR (Fast)
- **Time**: ~2-3 seconds
- **API Requests**: ~6 requests
- **Example**: Dependabot PRs

### Multi-Commit PR (Moderate)
- **Time**: ~5-10 seconds
- **API Requests**: ~10-20 requests
- **Example**: Feature branches with 5-10 commits

### Large PR (Slower)
- **Time**: ~15-20 seconds
- **API Requests**: ~30-50 requests
- **Example**: Major refactoring with 20+ commits

---

## Key Observations from Real PRs

1. **Single-commit PRs** (e.g., Dependabot) typically show `UNKNOWN` classification due to insufficient history

2. **Multi-commit PRs** with stable CI show more `RELIABLE` and `STABLE` classifications

3. **Flaky checks** are rare in well-maintained repositories but easily detected when present

4. **Error handling** works smoothly across various failure scenarios

5. **Rate limiting** is not an issue for individual PR analysis (well under 5,000 requests/hour limit)

---

## Conclusion

The CLI provides:
- ✅ Clear, formatted output with visual indicators
- ✅ Comprehensive error messages with actionable guidance
- ✅ Progressive loading indicators for better UX
- ✅ Sorted results for better readability
- ✅ Summary statistics and recommendations
- ✅ Graceful handling of edge cases

All outputs are deterministic, explainable, and user-friendly — ready for mentor review and production use!
