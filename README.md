# CI Reliability & Flakiness Analytics

**7-Day Pre-GSoC Feasibility Prototype for BLT GSoC 2026**

[![Tests](https://img.shields.io/badge/tests-19%20passed-success)]()
[![Python](https://img.shields.io/badge/python-3.7%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

## 🎯 Project Positioning

This project complements **Project E (PR Readiness Dashboard)** by analyzing **CI signal reliability** — helping maintainers understand which CI checks are trustworthy vs flaky, without overlapping the core review-state readiness pipeline.

**Focus:** CI confidence scoring, flakiness detection, and stability pattern analysis.

**Key Question:** *"Can we trust these CI signals?"* (vs Project E's *"Is the PR ready to merge?"*)

## ⭐ Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up GitHub token
echo "GITHUB_TOKEN=your_token_here" > pr-readiness-demo/.env

# Analyze a PR
python pr-readiness-demo/src/cli.py https://github.com/OWASP-BLT/BLT/pull/5618
```

## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and data flow
- **[FEATURES.md](FEATURES.md)** - Complete feature matrix (implemented vs planned)
- **[GSOC_PROPOSAL.md](GSOC_PROPOSAL.md)** - GSoC proposal integration guide

## ✨ Core Features

- ✅ PR URL parsing & GitHub API integration
- ✅ Check Runs & Commit Statuses aggregation
- ✅ Historical CI pattern analysis
- ✅ Flakiness detection & stability classification
- ✅ Confidence scoring (0-100) with explanations
- ✅ Professional CLI with error handling
- ✅ Unit test suite (19 tests, 100% pass rate)

## Key Capabilities

- ✅ Analyzes any public GitHub repository
- ✅ Detects flaky CI checks
- ✅ Classifies checks: RELIABLE/STABLE/FLAKY/UNSTABLE/UNKNOWN
- ✅ Provides explanations for every score
- ✅ 100% deterministic (no ML/AI)
- ✅ Production-ready error handling

## Testing

The project includes a comprehensive unit test suite:

```bash
# Run all tests (simple, one command)
python src/test.py

# Or use the test runner
python src/run_tests.py
```

**Test Coverage:**
- ✅ 6 parser tests (URL validation, edge cases)
- ✅ 7 CI aggregation tests (state logic, priority handling)
- ✅ 6 confidence scoring scenarios (all classifications)
- **Total: 19 tests with 100% pass rate**
- **No pytest required** - uses simple built-in assertions

## 🛡️ What This Demo Does NOT Do

_(By design — planned for full GSoC project)_

- ❌ No web dashboard or UI (CLI only)
- ❌ No machine learning or LLMs (deterministic heuristics only)
- ❌ No private repository support (public repos only)
- ❌ No time-series visualizations (text output only)
- ❌ No persistent storage (ephemeral analysis)
- ❌ No multi-PR batch analysis
- ❌ No review comment analysis (that's Project E's domain)

See **[FEATURES.md](FEATURES.md)** for complete list of implemented vs planned features.

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

## 🚀 Usage

### Command-Line Interface

```bash
# Analyze a Pull Request
python src/cli.py <github_pr_url>

# Show help documentation
python src/cli.py --help

# Show usage examples
python src/cli.py --examples

# Show version
python src/cli.py --version
```

### Real-World Examples

```bash
# Analyze OWASP BLT PR
python src/cli.py https://github.com/OWASP-BLT/BLT/pull/5618

# Analyze Zulip PR 
python src/cli.py https://github.com/zulip/zulip/pull/37753

# Analyze Django PR
python src/cli.py https://github.com/django/django/pull/18234
```

**Example Output:**
```
✅ Check: pytest-unit-tests
   Confidence: 100/100 - RELIABLE
   History: 15 runs (100% pass rate)

⚠️  Check: integration-tests
   Confidence: 35/100 - FLAKY
   History: 10 runs (60% pass rate, 5 transitions)

SUMMARY: 3 checks (1 Reliable, 1 Stable, 1 Flaky)
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

## 🏆 Project Status

✅ **7-day prototype complete** - Production-ready CI reliability analyzer

**Tested on:** Zulip, OWASP-BLT, Django, React repositories

## 🎓 For GSoC Mentors

**Quick Evaluation:**
```bash
git clone <repo-url> && cd PR_tracker/pr-readiness-demo
pip install -r requirements.txt
echo "GITHUB_TOKEN=your_token" > .env
python src/test.py  # Run tests
python src/cli.py https://github.com/OWASP-BLT/BLT/pull/5618  # Try it
```

**Review:** [ARCHITECTURE.md](ARCHITECTURE.md) | [FEATURES.md](FEATURES.md) | [GSOC_PROPOSAL.md](GSOC_PROPOSAL.md)

## 🚀 Next Steps (Full GSoC Project)

See **[GSOC_PROPOSAL.md](GSOC_PROPOSAL.md)** for detailed 13-week plan.

**Key Expansions**:
1. **Weeks 1-2**: PostgreSQL + Redis + FastAPI backend
2. **Weeks 3-4**: Multi-repository scanning and batch analysis
3. **Weeks 5-7**: Advanced analytics and trend analysis
4. **Weeks 8-10**: React dashboard with interactive visualizations
5. **Weeks 11-12**: GitHub App, webhooks, Slack/email notifications
6. **Week 13**: Polish, deployment, documentation

**Total**: 350 hours → Production CI reliability platform

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

This is a pre-GSoC prototype. For the full project:
1. Review [GSOC_PROPOSAL.md](GSOC_PROPOSAL.md)
2. Check open issues
3. Follow contribution guidelines
4. Submit PRs with tests

## 📧 Contact

For questions about this prototype or GSoC proposal:
- Open an issue in this repository
- Review the documentation files
- Check [EXAMPLES.md](EXAMPLES.md) for usage guidance

---

**Built with** ❤️ **as a GSoC 2026 feasibility prototype for OWASP BLT**
