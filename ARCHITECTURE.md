# Architecture & Design

**CI Reliability & Flakiness Analytics - System Architecture**

## Overview

This project implements a **deterministic, explainable CI reliability analysis pipeline** that ingests GitHub Pull Requests and produces confidence scores, flakiness detection, and stability classifications without using machine learning or LLMs.

## Design Principles

1. **Deterministic Logic**: All decisions are rule-based and reproducible
2. **Explainable Results**: Every score includes human-readable reasoning
3. **No ML/AI**: Uses heuristics and statistical patterns only
4. **API-First**: Built on GitHub REST API with no web scraping
5. **Graceful Degradation**: Handles edge cases without crashing
6. **Test-Driven**: 22+ unit tests ensure reliability

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Layer                           │
│                        (cli.py)                             │
│  • Argument parsing (--help, --examples, --version)         │
│  • User interaction and progress indicators                 │
│  • Error formatting and guidance                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Input Validation                         │
│                      (parser.py)                            │
│  • URL pattern matching                                     │
│  • Extract owner/repo/PR number                             │
│  • Validate format                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   GitHub API Client                         │
│                  (github/client.py)                         │
│  • Authentication (PAT)                                     │
│  • Rate limit handling                                      │
│  • Request timeout management                               │
│  • Centralized error handling                               │
│  • API endpoints:                                           │
│    - PR metadata                                            │
│    - Check runs                                             │
│    - Commit statuses                                        │
│    - PR commits                                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
┌──────────────────────┐   ┌──────────────────────┐
│   CI Aggregation     │   │  Historical Analysis │
│   (github/ci.py)     │   │  (github/history.py) │
│                      │   │                      │
│ • Unified CI state   │   │ • Fetch all commits  │
│ • Check runs         │   │ • Track CI outcomes  │
│ • Commit statuses    │   │ • Pattern detection  │
│ • Priority: FAIL >   │   │ • Per-check history  │
│   PENDING > PASS     │   │                      │
└──────────────────────┘   └──────────┬───────────┘
                                      │
                                      ▼
                          ┌──────────────────────┐
                          │ Confidence Scoring   │
                          │ (github/confidence.py│
                          │                      │
                          │ • Flakiness detect   │
                          │ • Stability metrics  │
                          │ • 0-100 scoring      │
                          │ • Classification     │
                          │ • Explanation gen    │
                          └──────────┬───────────┘
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │   Output Formatting  │
                          │   (cli.py)           │
                          │                      │
                          │ • Visual indicators  │
                          │ • Sorted by score    │
                          │ • Summary stats      │
                          │ • Recommendations    │
                          └──────────────────────┘
```

## Module Descriptions

### 1. CLI Layer (`cli.py`)

**Responsibility**: User interface and interaction

**Key Functions**:
- `print_help()`: Display comprehensive help
- `print_examples()`: Show usage examples
- `print_version()`: Version information
- `main()`: Orchestrate the entire analysis pipeline

**Features**:
- Command-line argument parsing
- Progressive loading indicators (📥 🔍 ✨)
- Professional formatting with emoji indicators
- Comprehensive error handling with contextual guidance
- Sorted output by confidence score

### 2. Input Validation (`parser.py`)

**Responsibility**: Parse and validate PR URLs

**Key Functions**:
- `parse_pr_url(url)`: Extract owner, repo, PR number

**Validation Rules**:
- Must be GitHub URL
- Must be `/pull/` endpoint (not `/issues/`)
- Must have numeric PR number
- Supports hyphens and numbers in owner/repo names

**Error Handling**:
- Raises `ValueError` for invalid URLs
- Clear error messages explaining expected format

### 3. GitHub API Client (`github/client.py`)

**Responsibility**: All GitHub API interactions

**Key Components**:
- `GitHubClient`: Main API client class
- `_check_response()`: Centralized error handling
- `_handle_rate_limit()`: Smart rate limit detection

**API Methods**:
- `get_pull_request()`: Fetch PR metadata
- `get_pr_head_sha()`: Get latest commit SHA
- `get_check_runs()`: Fetch Check Runs (GitHub Actions, etc.)
- `get_commit_statuses()`: Fetch Commit Statuses (legacy CI)
- `get_pr_commits()`: Fetch all commits in PR

**Error Handling**:
- 404: Resource not found
- 403: Rate limit or access denied (differentiated)
- 500+: Server errors
- Timeout: Network timeouts (10s default)
- Connection errors: Network failures

### 4. CI Aggregation (`github/ci.py`)

**Responsibility**: Unified CI state determination

**Function**: `aggregate_ci(check_runs, statuses)`

**Logic**:
1. Combine Check Runs and Commit Statuses
2. Check for failures (failure, cancelled, timed_out, error) → FAIL
3. Check for pending (queued, in_progress, pending) → PENDING
4. All passed → PASS
5. No CI data → NO_CI

**Priority**: `FAIL > PENDING > PASS > NO_CI`

### 5. Historical Analysis (`github/history.py`)

**Responsibility**: Track CI patterns across commits

**Function**: `analyze_ci_reliability(client, owner, repo, pr_number)`

**Algorithm**:
1. Fetch all commits from the PR
2. For each commit, fetch CI outcomes
3. Group by check name
4. Track pass/fail patterns
5. Call confidence scoring for each check

**Data Structure**:
```python
{
    "check_name": {
        "outcomes": [
            {"outcome": "PASS", "sha": "abc123"},
            {"outcome": "FAIL", "sha": "def456"}
        ]
    }
}
```

### 6. Confidence Scoring (`github/confidence.py`)

**Responsibility**: Calculate confidence scores and classify checks

**Function**: `calculate_confidence_score(outcomes)`

**Classification Priority** (checked in order):
1. **RELIABLE (90-100)**: 
   - 10+ runs, all passes
   - OR 15+ runs with 93%+ pass rate
   
2. **STABLE (70-89)**:
   - 3+ consecutive passes at the end
   - 5+ consecutive passes → 85 score
   - 3-4 consecutive passes → 75 score

3. **FLAKY (20-50)**:
   - Pass/fail transition rate ≥ 35%
   - Indicates alternating outcomes
   - Score inversely related to pass rate

4. **UNSTABLE (10-30)**:
   - 3+ consecutive failures
   - OR pass rate < 50%
   - Score based on pass rate

5. **UNKNOWN (40-60)**:
   - < 3 runs (insufficient data)
   - All pending/incomplete
   - Score: 50 (neutral)

**Metrics Calculated**:
- Total runs
- Passes / Failures
- Pass rate percentage
- Consecutive passes / failures
- Pass/fail transitions (for flakiness)

**Output**:
```python
{
    "classification": "FLAKY",
    "confidence_score": 35,
    "reason": "Inconsistent behavior: 5 pass/fail transitions detected",
    "current_status": "PASS",
    "metrics": {
        "total_runs": 10,
        "passes": 6,
        "failures": 4,
        "pass_rate": 60.0,
        "consecutive_passes": 1,
        "consecutive_failures": 0,
        "transitions": 5
    }
}
```

## Data Flow

### High-Level Flow

```
User Input (PR URL)
    ↓
Parse & Validate
    ↓
Fetch PR Metadata ← → GitHub API
    ↓
Fetch Current CI Status ← → GitHub API
    ↓
Aggregate CI State
    ↓
Fetch All Commits ← → GitHub API
    ↓
Fetch CI for Each Commit ← → GitHub API
    ↓
Group by Check Name
    ↓
Calculate Confidence Score (per check)
    ↓
Format & Display Results
```

### Detailed Data Flow

**Phase 1: Initialization**
1. User provides PR URL
2. CLI parses command-line arguments
3. Parser validates URL format
4. GitHubClient initializes with PAT

**Phase 2: PR Metadata**
1. Client fetches PR data
2. Extract: title, author, state, commits, files
3. Display PR metadata section

**Phase 3: Current CI Status**
1. Extract head commit SHA
2. Fetch Check Runs for SHA
3. Fetch Commit Statuses for SHA
4. Aggregate into unified state
5. Display CI status section

**Phase 4: Historical Analysis**
1. Fetch all commits in PR
2. For each commit:
   - Fetch Check Runs
   - Fetch Commit Statuses
   - Extract outcomes per check
3. Group outcomes by check name
4. Build historical dataset

**Phase 5: Confidence Scoring**
1. For each check name:
   - Pass outcomes to scoring engine
   - Calculate metrics
   - Determine classification
   - Generate explanation
2. Sort by confidence score (descending)

**Phase 6: Output**
1. Display each check with:
   - Emoji indicator
   - Current status
   - Confidence score
   - Classification
   - History metrics
   - Trend analysis
   - Explanation
2. Display summary statistics
3. Provide overall recommendation

## Error Handling Strategy

### Layered Error Handling

1. **API Layer** (`client.py`):
   - Catches HTTP errors
   - Detects rate limits
   - Handles timeouts
   - Raises specific exceptions

2. **CLI Layer** (`cli.py`):
   - Catches typed exceptions
   - Formats error messages
   - Provides troubleshooting guidance
   - Exits with appropriate codes

### Exception Types

- `ValueError`: Invalid input (URL format)
- `PermissionError`: Authentication issues
- `ConnectionError`: Network/rate limit issues
- `KeyError`: Data structure issues
- `RuntimeError`: Unexpected errors

### Error Messages

All errors include:
- Clear description of what went wrong
- Possible causes
- Actionable next steps
- Example of correct usage (when applicable)

## Performance Considerations

### API Rate Limits

- GitHub API: 5,000 requests/hour (authenticated)
- Requests per PR analysis:
  - 1 for PR metadata
  - 1 for Check Runs (current)
  - 1 for Commit Statuses (current)
  - 1 for PR commits list
  - N for historical CI (N = number of commits)
  
**Total**: ~4 + N requests per PR

### Optimization Strategies

1. **Batch Fetching**: Get all commits in one request
2. **Timeouts**: 10-second timeout prevents hanging
3. **Early Exit**: Stop on first error rather than continuing
4. **Caching**: Could cache commit data (future enhancement)

### Scalability

Current implementation:
- **Single PR**: < 10 seconds typically
- **10 commits**: ~15-20 requests
- **Rate limit safe**: Far below 5,000/hour limit

Future considerations:
- Implement request caching
- Batch analysis of multiple PRs
- Parallel request processing

## Testing Strategy

### Unit Test Coverage

1. **Parser Tests** (10 tests):
   - Valid URL formats
   - Invalid URL formats
   - Edge cases (trailing slash, special characters)

2. **CI Aggregation Tests** (12 tests):
   - No CI scenario
   - All passing
   - Any failing (priority)
   - Pending states
   - Mixed check runs and statuses

3. **Confidence Scoring Tests** (13+ scenarios):
   - All classification types
   - Boundary conditions
   - Edge cases (no data, all pending)

### Test Principles

- **Deterministic**: No randomness, reproducible results
- **Isolated**: No external dependencies or API calls
- **Fast**: All tests run in < 5 seconds
- **Clear**: Descriptive names and assertions

## Security Considerations

### Authentication

- GitHub PAT stored in `.env` (gitignored)
- Token required for API access
- Supports public repositories only (private requires different scope)

### Data Privacy

- No data storage: All analysis is ephemeral
- No logging of sensitive information
- No user data collection

### Input Validation

- Strict URL parsing prevents injection
- No shell command execution
- No file system writes (except `.env`)

## Future Enhancements

### Immediate (GSoC Scope)

1. **Multi-Repository Analysis**: Aggregate across projects
2. **Cross-Project Patterns**: Find common flaky checks
3. **Trend Visualization**: Time-series graphs
4. **Caching Layer**: Redis for historical data
5. **Web Dashboard**: Interactive UI

### Long-Term

1. **Workflow Recommendations**: Suggest CI improvements
2. **Integration with Project E**: Merge readiness correlation
3. **Slack/Email Notifications**: Alert on flaky checks
4. **Historical Database**: Track flakiness over time
5. **Cost Analysis**: CI runtime and cost metrics

## Deployment Considerations

### Requirements

- Python 3.10+
- Dependencies: `requests`, `python-dotenv`
- GitHub Personal Access Token
- Internet connection

### Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure token
echo "GITHUB_TOKEN=your_token" > .env

# Run tests
python src/run_tests.py

# Run analysis
python src/cli.py <pr_url>
```

### Production Readiness

✅ Error handling complete
✅ Input validation robust
✅ Edge cases covered
✅ Test suite comprehensive
✅ Documentation complete

⚠️ Not yet implemented:
- Rate limit backoff/retry
- Persistent caching
- Multi-PR batch analysis
- Web interface

## Conclusion

This architecture demonstrates:
- Clean separation of concerns
- Deterministic, explainable logic
- Robust error handling
- Comprehensive testing
- Clear upgrade path to full GSoC project

The system is **production-ready for CLI usage** and serves as a strong **feasibility prototype** for the full CI Reliability Analytics platform.
