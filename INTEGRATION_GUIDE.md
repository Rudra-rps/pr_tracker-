# PR Review Progress Tracking - Integration Guide

**How to add Review Tracking to complement CI Confidence Scoring**

## 🎯 Overview

This guide shows how to integrate **Review Progress Tracking** with existing **CI Confidence Scoring** to create a comprehensive PR Readiness system.

**Goal:** Answer "Is this PR ready to merge?" by combining:
- ✅ CI reliability signals (already implemented)
- ✅ Review feedback loops (new feature)
- ✅ Author responsiveness (new feature)
- ✅ Progress state tracking (new feature)

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                  PR Analysis Engine                  │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────────────┐      ┌──────────────────┐    │
│  │  CI Module       │      │  Review Module   │    │
│  │  (Existing)      │      │  (NEW)           │    │
│  ├──────────────────┤      ├──────────────────┤    │
│  │ • Check Runs     │      │ • Review Comments│    │
│  │ • Commit Status  │      │ • Timeline       │    │
│  │ • Flakiness      │      │ • Feedback Loops │    │
│  │ • Confidence     │      │ • Responsiveness │    │
│  └────────┬─────────┘      └────────┬─────────┘    │
│           │                         │               │
│           └──────────┬──────────────┘               │
│                      ▼                               │
│           ┌──────────────────────┐                  │
│           │  Readiness Scorer    │                  │
│           │  (NEW)               │                  │
│           ├──────────────────────┤                  │
│           │ • Combined Score     │                  │
│           │ • Merge Readiness    │                  │
│           │ • Blockers           │                  │
│           │ • Recommendations    │                  │
│           └──────────────────────┘                  │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 Module Structure

### Files to Create

```
src/github/
├── ci.py                    # ✅ Existing - CI reliability
├── confidence.py            # ✅ Existing - CI scoring
├── history.py              # ✅ Existing - Historical patterns
├── review.py               # ❌ NEW - Review tracking
├── responsiveness.py       # ❌ NEW - Author response analysis
├── readiness.py            # ❌ NEW - Combined PR readiness
└── timeline.py             # ❌ NEW - Event timeline builder
```

---

## 📋 Step-by-Step Integration Flow

### **Phase 1: GitHub API Integration** (2-3 hours)

#### 1.1 Add Review API Methods to GitHubClient

**File:** `src/github/client.py`

```python
def get_pr_reviews(self, owner, repo, number):
    """Fetch all PR reviews"""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{number}/reviews"
    try:
        r = self.session.get(url, timeout=10)
    except requests.exceptions.Timeout:
        raise ConnectionError("Request timed out while fetching reviews.")
    self._check_response(r, "Fetching PR reviews")
    return r.json()

def get_pr_review_comments(self, owner, repo, number):
    """Fetch all review comments (inline code comments)"""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{number}/comments"
    try:
        r = self.session.get(url, timeout=10)
    except requests.exceptions.Timeout:
        raise ConnectionError("Request timed out while fetching review comments.")
    self._check_response(r, "Fetching review comments")
    return r.json()

def get_pr_issue_comments(self, owner, repo, number):
    """Fetch general issue comments on the PR"""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/issues/{number}/comments"
    try:
        r = self.session.get(url, timeout=10)
    except requests.exceptions.Timeout:
        raise ConnectionError("Request timed out while fetching issue comments.")
    self._check_response(r, "Fetching issue comments")
    return r.json()

def get_pr_timeline(self, owner, repo, number):
    """Fetch full PR timeline (reviews, commits, comments, etc)"""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/issues/{number}/timeline"
    headers = {"Accept": "application/vnd.github.mockingbird-preview+json"}
    try:
        r = self.session.get(url, headers=headers, timeout=15)
    except requests.exceptions.Timeout:
        raise ConnectionError("Request timed out while fetching timeline.")
    self._check_response(r, "Fetching PR timeline")
    return r.json()
```

**API Endpoints Used:**
- `GET /repos/{owner}/{repo}/pulls/{number}/reviews` - PR reviews
- `GET /repos/{owner}/{repo}/pulls/{number}/comments` - Review comments
- `GET /repos/{owner}/{repo}/issues/{number}/comments` - Issue comments
- `GET /repos/{owner}/{repo}/issues/{number}/timeline` - Full timeline

---

### **Phase 2: Timeline Builder** (2-3 hours)

#### 2.1 Create Timeline Module

**File:** `src/github/timeline.py`

```python
from datetime import datetime
from typing import List, Dict

def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse GitHub ISO timestamp"""
    return datetime.strptime(timestamp_str.replace('Z', '+00:00'), '%Y-%m-%dT%H:%M:%S%z')

def build_timeline(client, owner: str, repo: str, number: str) -> List[Dict]:
    """
    Build unified timeline of all PR events
    
    Returns list of events sorted chronologically:
    - commits
    - review comments
    - reviews (approved/changes_requested/commented)
    - issue comments
    """
    events = []
    
    # Fetch all data sources
    commits = client.get_pr_commits(owner, repo, number)
    reviews = client.get_pr_reviews(owner, repo, number)
    review_comments = client.get_pr_review_comments(owner, repo, number)
    issue_comments = client.get_pr_issue_comments(owner, repo, number)
    
    # Add commits
    for commit in commits:
        events.append({
            'type': 'commit',
            'timestamp': parse_timestamp(commit['commit']['author']['date']),
            'author': commit['commit']['author']['name'],
            'sha': commit['sha'][:7],
            'message': commit['commit']['message'].split('\n')[0]
        })
    
    # Add reviews
    for review in reviews:
        if review['state'] == 'PENDING':
            continue  # Skip pending/draft reviews
        events.append({
            'type': 'review',
            'timestamp': parse_timestamp(review['submitted_at']),
            'author': review['user']['login'],
            'state': review['state'],  # APPROVED, CHANGES_REQUESTED, COMMENTED
            'body': review['body'] or ''
        })
    
    # Add review comments (inline code comments)
    for comment in review_comments:
        events.append({
            'type': 'review_comment',
            'timestamp': parse_timestamp(comment['created_at']),
            'author': comment['user']['login'],
            'body': comment['body'],
            'path': comment['path'],
            'in_reply_to': comment.get('in_reply_to_id')
        })
    
    # Add issue comments
    for comment in issue_comments:
        events.append({
            'type': 'issue_comment',
            'timestamp': parse_timestamp(comment['created_at']),
            'author': comment['user']['login'],
            'body': comment['body']
        })
    
    # Sort by timestamp
    events.sort(key=lambda x: x['timestamp'])
    
    return events
```

---

### **Phase 3: Review Analysis** (3-4 hours)

#### 3.1 Create Review Module

**File:** `src/github/review.py`

```python
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

def analyze_review_progress(timeline: List[Dict], pr_author: str) -> Dict:
    """
    Analyze review feedback loops and author responsiveness
    
    Returns:
    {
        'feedback_loops': [
            {
                'reviewer': 'john',
                'feedback_time': datetime,
                'author_responded': True,
                'response_time': datetime,
                'response_type': 'commit' | 'comment',
                'resolved': True
            }
        ],
        'awaiting_author': Bool,
        'awaiting_reviewer': Bool,
        'stale_feedback': List[Dict],
        'review_state': 'APPROVED' | 'CHANGES_REQUESTED' | 'COMMENTED' | 'PENDING'
    }
    """
    feedback_loops = []
    latest_review_state = None
    last_reviewer_action = None
    last_author_action = None
    
    # Iterate through timeline to detect feedback patterns
    for event in timeline:
        author = event['author']
        timestamp = event['timestamp']
        
        # Track reviewer actions (reviews and comments)
        if event['type'] in ['review', 'review_comment'] and author != pr_author:
            last_reviewer_action = timestamp
            
            if event['type'] == 'review':
                latest_review_state = event['state']
            
            # Create feedback loop entry
            feedback_loops.append({
                'reviewer': author,
                'feedback_time': timestamp,
                'feedback_type': event['type'],
                'author_responded': False,  # Will update on next author action
                'response_time': None,
                'response_type': None
            })
        
        # Track author actions (commits and comments)
        elif author == pr_author and event['type'] in ['commit', 'issue_comment', 'review_comment']:
            last_author_action = timestamp
            
            # Check if this responds to pending feedback
            for loop in reversed(feedback_loops):
                if not loop['author_responded'] and loop['feedback_time'] < timestamp:
                    loop['author_responded'] = True
                    loop['response_time'] = timestamp
                    loop['response_type'] = event['type']
                    loop['response_delay_hours'] = (timestamp - loop['feedback_time']).total_seconds() / 3600
                    break
    
    # Determine current state
    awaiting_author = (
        latest_review_state == 'CHANGES_REQUESTED' or
        (last_reviewer_action and 
         (not last_author_action or last_reviewer_action > last_author_action))
    )
    
    awaiting_reviewer = (
        not awaiting_author and
        (not last_reviewer_action or last_author_action > last_reviewer_action)
    )
    
    # Find stale feedback (older than 3 days without response)
    now = datetime.now(timeline[0]['timestamp'].tzinfo)
    stale_feedback = [
        loop for loop in feedback_loops
        if not loop['author_responded'] and 
           (now - loop['feedback_time']) > timedelta(days=3)
    ]
    
    return {
        'feedback_loops': feedback_loops,
        'total_feedback_count': len(feedback_loops),
        'responded_count': sum(1 for loop in feedback_loops if loop['author_responded']),
        'response_rate': sum(1 for loop in feedback_loops if loop['author_responded']) / len(feedback_loops) if feedback_loops else 1.0,
        'awaiting_author': awaiting_author,
        'awaiting_reviewer': awaiting_reviewer,
        'stale_feedback': stale_feedback,
        'latest_review_state': latest_review_state,
        'last_reviewer_action': last_reviewer_action,
        'last_author_action': last_author_action
    }


def classify_review_health(review_data: Dict) -> Tuple[str, int]:
    """
    Classify review health and assign score
    
    Returns: (classification, score)
    - ACTIVE: 80-100 - Good progress, responsive
    - AWAITING_AUTHOR: 40-70 - Needs author response
    - AWAITING_REVIEWER: 60-80 - Waiting on reviewers
    - STALLED: 0-30 - No activity or unaddressed feedback
    - APPROVED: 90-100 - Reviews approved
    """
    response_rate = review_data['response_rate']
    stale_count = len(review_data['stale_feedback'])
    awaiting_author = review_data['awaiting_author']
    awaiting_reviewer = review_data['awaiting_reviewer']
    latest_state = review_data['latest_review_state']
    
    # Approved state
    if latest_state == 'APPROVED':
        return 'APPROVED', 95
    
    # Stalled (has stale feedback)
    if stale_count > 0:
        score = max(10, 50 - (stale_count * 15))
        return 'STALLED', score
    
    # Awaiting author with poor response rate
    if awaiting_author and response_rate < 0.5:
        return 'AWAITING_AUTHOR', 35
    
    # Awaiting author with good response rate
    if awaiting_author:
        return 'AWAITING_AUTHOR', 55
    
    # Awaiting reviewer
    if awaiting_reviewer:
        score = 70 + int(response_rate * 20)
        return 'AWAITING_REVIEWER', score
    
    # Active (good back and forth)
    if response_rate > 0.7:
        return 'ACTIVE', 85
    
    return 'ACTIVE', 70
```

---

### **Phase 4: Combined Readiness Score** (2-3 hours)

#### 4.1 Create Readiness Module

**File:** `src/github/readiness.py`

```python
from typing import Dict, List

def calculate_pr_readiness(ci_results: Dict, review_health: Dict) -> Dict:
    """
    Calculate overall PR readiness score combining CI and review health
    
    Args:
        ci_results: Output from confidence.calculate_confidence()
        review_health: Output from review.classify_review_health()
    
    Returns:
        {
            'overall_score': 0-100,
            'ci_score': 0-100,
            'review_score': 0-100,
            'classification': str,
            'merge_ready': bool,
            'blockers': List[str],
            'warnings': List[str],
            'recommendations': List[str]
        }
    """
    # Extract scores
    ci_scores = [check['confidence'] for check in ci_results]
    avg_ci_score = sum(ci_scores) / len(ci_scores) if ci_scores else 50
    
    review_classification, review_score = review_health
    
    # Weight: 60% CI, 40% Review (adjust as needed)
    overall_score = (avg_ci_score * 0.6) + (review_score * 0.4)
    
    # Identify blockers
    blockers = []
    warnings = []
    recommendations = []
    
    # CI blockers
    failed_checks = [c for c in ci_results if c['status'] == 'FAIL']
    flaky_checks = [c for c in ci_results if c['classification'] == 'FLAKY']
    
    if failed_checks:
        blockers.append(f"{len(failed_checks)} CI check(s) failing")
    
    if flaky_checks:
        warnings.append(f"{len(flaky_checks)} flaky check(s) detected")
        recommendations.append("Investigate flaky checks before merging")
    
    # Review blockers
    if review_classification == 'AWAITING_AUTHOR':
        blockers.append("Awaiting author response to feedback")
        recommendations.append("Address reviewer comments and push updates")
    
    if review_classification == 'STALLED':
        blockers.append("PR has stale unaddressed feedback")
        recommendations.append("Review and respond to old comments")
    
    if review_classification == 'AWAITING_REVIEWER':
        warnings.append("Awaiting reviewer approval")
        recommendations.append("Ping reviewers or request re-review")
    
    # Determine if merge ready
    merge_ready = (
        overall_score >= 70 and
        len(blockers) == 0 and
        review_classification in ['APPROVED', 'AWAITING_REVIEWER', 'ACTIVE']
    )
    
    # Overall classification
    if merge_ready:
        classification = 'READY_TO_MERGE'
    elif overall_score >= 60:
        classification = 'NEARLY_READY'
    elif overall_score >= 40:
        classification = 'NEEDS_WORK'
    else:
        classification = 'NOT_READY'
    
    return {
        'overall_score': round(overall_score, 1),
        'ci_score': round(avg_ci_score, 1),
        'review_score': review_score,
        'classification': classification,
        'merge_ready': merge_ready,
        'blockers': blockers,
        'warnings': warnings,
        'recommendations': recommendations
    }
```

---

### **Phase 5: CLI Integration** (2-3 hours)

#### 5.1 Update Main CLI

**File:** `src/cli.py`

Add new import and function call:

```python
from github.timeline import build_timeline
from github.review import analyze_review_progress, classify_review_health
from github.readiness import calculate_pr_readiness

def main():
    # ... existing PR fetching code ...
    
    # Existing CI analysis
    ci_results = analyze_ci_reliability(...)
    
    # NEW: Review analysis
    print("🔍 Analyzing review feedback loops...")
    timeline = build_timeline(client, owner, repo, number)
    review_data = analyze_review_progress(timeline, pr_data['user']['login'])
    review_health = classify_review_health(review_data)
    
    # NEW: Combined readiness
    print("✨ Calculating PR readiness...")
    readiness = calculate_pr_readiness(ci_results, review_health)
    
    # Display results
    print_ci_results(ci_results)  # Existing
    print_review_analysis(review_data, review_health)  # NEW
    print_readiness_summary(readiness)  # NEW
```

#### 5.2 Create Display Functions

```python
def print_review_analysis(review_data: Dict, health: Tuple[str, int]):
    """Display review progress analysis"""
    classification, score = health
    
    print("\n" + "="*70)
    print("📝 REVIEW PROGRESS ANALYSIS")
    print("="*70)
    
    icon_map = {
        'APPROVED': '✅',
        'ACTIVE': '🟢',
        'AWAITING_REVIEWER': '🟡',
        'AWAITING_AUTHOR': '🟠',
        'STALLED': '🔴'
    }
    
    print(f"\n{icon_map.get(classification, '📊')} Review Health: {classification}")
    print(f"   Score: {score}/100")
    print(f"   Response Rate: {review_data['response_rate']:.0%}")
    print(f"   Feedback Loops: {review_data['responded_count']}/{review_data['total_feedback_count']} addressed")
    
    if review_data['stale_feedback']:
        print(f"\n⚠️  Stale Feedback:")
        for feedback in review_data['stale_feedback'][:3]:  # Show max 3
            days_old = (datetime.now() - feedback['feedback_time']).days
            print(f"   • {feedback['reviewer']}: {days_old} days old, no response")
    
    print()


def print_readiness_summary(readiness: Dict):
    """Display overall PR readiness"""
    print("\n" + "="*70)
    print("🎯 PR READINESS SUMMARY")
    print("="*70)
    
    classification_icons = {
        'READY_TO_MERGE': '✅',
        'NEARLY_READY': '🟡',
        'NEEDS_WORK': '🟠',
        'NOT_READY': '🔴'
    }
    
    icon = classification_icons.get(readiness['classification'], '📊')
    
    print(f"\n{icon} Classification: {readiness['classification']}")
    print(f"   Overall Score: {readiness['overall_score']}/100")
    print(f"   ├─ CI Confidence: {readiness['ci_score']}/100")
    print(f"   └─ Review Health: {readiness['review_score']}/100")
    print(f"\n   Merge Ready: {'✅ YES' if readiness['merge_ready'] else '❌ NO'}")
    
    if readiness['blockers']:
        print(f"\n🚫 BLOCKERS:")
        for blocker in readiness['blockers']:
            print(f"   • {blocker}")
    
    if readiness['warnings']:
        print(f"\n⚠️  WARNINGS:")
        for warning in readiness['warnings']:
            print(f"   • {warning}")
    
    if readiness['recommendations']:
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in readiness['recommendations']:
            print(f"   • {rec}")
    
    print("\n" + "="*70)
```

---

### **Phase 6: Testing** (3-4 hours)

#### 6.1 Create Tests

**File:** `src/test_review.py`

```python
def test_review_timeline_parsing():
    """Test timeline building"""
    # Mock timeline data
    timeline = [
        {'type': 'commit', 'author': 'author', 'timestamp': datetime(2024, 1, 1, 10, 0)},
        {'type': 'review_comment', 'author': 'reviewer', 'timestamp': datetime(2024, 1, 1, 11, 0)},
        {'type': 'commit', 'author': 'author', 'timestamp': datetime(2024, 1, 1, 12, 0)}
    ]
    
    result = analyze_review_progress(timeline, 'author')
    
    assert result['total_feedback_count'] == 1
    assert result['responded_count'] == 1
    assert result['response_rate'] == 1.0
    print("✓ Timeline parsing test passed")


def test_stale_feedback_detection():
    """Test stale feedback identification"""
    now = datetime.now()
    old_time = now - timedelta(days=5)
    
    timeline = [
        {'type': 'review_comment', 'author': 'reviewer', 'timestamp': old_time}
    ]
    
    result = analyze_review_progress(timeline, 'author')
    
    assert len(result['stale_feedback']) == 1
    print("✓ Stale feedback detection test passed")


def test_readiness_scoring():
    """Test combined readiness calculation"""
    # Perfect CI, approved review
    ci_results = [
        {'confidence': 100, 'status': 'PASS', 'classification': 'RELIABLE'}
    ]
    review_health = ('APPROVED', 95)
    
    readiness = calculate_pr_readiness(ci_results, review_health)
    
    assert readiness['merge_ready'] == True
    assert readiness['overall_score'] >= 90
    print("✓ Readiness scoring test passed")


if __name__ == "__main__":
    test_review_timeline_parsing()
    test_stale_feedback_detection()
    test_readiness_scoring()
    print("\n✅ All review tests passed!")
```

---

## 🔄 Data Flow Diagram

```
GitHub PR
    │
    ├──> fetch_pr_data()
    │    ├─> CI checks ──────────────┐
    │    ├─> Reviews                 │
    │    ├─> Comments                │
    │    └─> Commits                 │
    │                                 ▼
    ├──> build_timeline()      [CI Analysis]
    │    └─> Sorted events           │
    │                            confidence.py
    ▼                          history.py
[Review Analysis]                   │
    review.py                       │
    │                               │
    ├─> Feedback loops              │
    ├─> Response detection          │
    ├─> Stale feedback              │
    └─> Health classification       │
              │                     │
              └──────┬──────────────┘
                     ▼
            [Readiness Scorer]
              readiness.py
                     │
                     ├─> Overall score
                     ├─> Blockers
                     ├─> Warnings
                     └─> Recommendations
                           │
                           ▼
                    [CLI Display]
                      cli.py
```

---

## 🎯 Integration Checklist

### For Your Existing Codebase
- [ ] Add new API methods to `client.py`
- [ ] Create `timeline.py` module
- [ ] Create `review.py` module
- [ ] Create `readiness.py` module
- [ ] Update `cli.py` main flow
- [ ] Add display functions
- [ ] Create tests for new modules
- [ ] Update documentation

### For BLT/Leaf Repository Integration
- [ ] Clone/fork their repository
- [ ] Locate their PR analysis code
- [ ] Map their data structures to your modules
- [ ] Add GitHub API calls (if not present)
- [ ] Integrate timeline building
- [ ] Plug in review analysis
- [ ] Combine with their existing scoring
- [ ] Add CLI/API endpoints
- [ ] Test with real BLT PRs
- [ ] Submit PR with tests and docs

---

## 📦 Portable Module Package

You can package these modules as a standalone library:

```python
# pr_readiness/__init__.py
from .timeline import build_timeline
from .review import analyze_review_progress, classify_review_health
from .readiness import calculate_pr_readiness

__all__ = [
    'build_timeline',
    'analyze_review_progress',
    'classify_review_health',
    'calculate_pr_readiness'
]
```

**Usage in any codebase:**

```python
from pr_readiness import build_timeline, analyze_review_progress, classify_review_health, calculate_pr_readiness

# In your existing code:
timeline = build_timeline(github_client, owner, repo, pr_number)
review_data = analyze_review_progress(timeline, pr_author)
review_health = classify_review_health(review_data)

# Combine with your CI results:
readiness = calculate_pr_readiness(your_ci_results, review_health)
```

---

## 🎓 Benefits vs "gtg" Tool

| Feature | gtg | Your Solution |
|---------|-----|---------------|
| Comment Analysis | ❌ "Ambiguous" flag only | ✅ Tracks actual feedback loops |
| Progress Tracking | ❌ No | ✅ Detects response to feedback |
| Author Responsiveness | ❌ No | ✅ Response rate & timing |
| Stale Feedback Detection | ❌ No | ✅ Identifies unaddressed comments |
| Combined CI + Review | ❌ No | ✅ Unified readiness score |
| Actionable Recommendations | ❌ Limited | ✅ Context-aware suggestions |

---

## 🚀 Next Steps

1. **Implement locally** - Add modules to your PR_tracker project
2. **Test with real PRs** - Validate on Zulip, BLT, Django PRs
3. **Create PR to BLT/Leaf** - Package and submit integration
4. **Document integration** - Provide examples and API docs
5. **Iterate based on feedback** - Refine scoring algorithm

---

## 📝 Example Output

```bash
$ python cli.py https://github.com/OWASP-BLT/BLT/pull/5618

======================================================================
                    PR READINESS ANALYSIS
======================================================================

📥 Analyzing PR #5618: Fix authentication bug

🔍 Analyzing CI reliability...
✅ pytest: 100/100 - RELIABLE
✅ eslint: 95/100 - RELIABLE  
⚠️  e2e-tests: 45/100 - FLAKY

📝 REVIEW PROGRESS ANALYSIS
======================================================================
🟡 Review Health: AWAITING_REVIEWER
   Score: 75/100
   Response Rate: 100%
   Feedback Loops: 3/3 addressed
   
   Last Activity:
   • Author pushed fix (2 hours ago)
   • Awaiting re-review from @maintainer

🎯 PR READINESS SUMMARY
======================================================================
🟡 Classification: NEARLY_READY
   Overall Score: 78.0/100
   ├─ CI Confidence: 80.0/100
   └─ Review Health: 75/100
   
   Merge Ready: ❌ NO

⚠️  WARNINGS:
   • 1 flaky check detected
   • Awaiting reviewer approval

💡 RECOMMENDATIONS:
   • Investigate e2e-tests flakiness
   • Ping reviewers for re-review
   • Consider re-running flaky checks
======================================================================
```

---

## 💡 Customization Points

You can adjust scoring weights in `readiness.py`:

```python
# Adjust importance of CI vs Review
overall_score = (avg_ci_score * 0.6) + (review_score * 0.4)

# Make CI more important (70/30):
overall_score = (avg_ci_score * 0.7) + (review_score * 0.3)

# Equal weight (50/50):
overall_score = (avg_ci_score * 0.5) + (review_score * 0.5)
```

Adjust staleness threshold:

```python
# Currently 3 days - make it 7 days:
stale_feedback = [
    loop for loop in feedback_loops
    if not loop['author_responded'] and 
       (now - loop['feedback_time']) > timedelta(days=7)  # Changed
]
```

---

**This guide provides everything needed to integrate review tracking into any codebase! 🚀**
