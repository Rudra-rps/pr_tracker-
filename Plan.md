Pre-GSoC Mini Demo Roadmap

Project E — PR Readiness Tracker

Objective

Develop a minimal but functional PR Readiness Tracker that ingests a GitHub Pull Request and deterministically reports whether it is READY, ACTION_REQUIRED, or CI_FAILING based on CI state and unresolved review feedback.

This prototype validates feasibility, scope control, and execution capability ahead of the full 350-hour project.

Overall Scope of Mini Demo
Included

Public GitHub Pull Requests

CI aggregation (Check Runs + Commit Statuses)

Review comment and thread resolution tracking

Deterministic readiness classification

CLI-based interface (lightweight, reproducible)

Explicitly Out of Scope

Private repositories

Machine learning or LLMs

Automated blocking or enforcement

Security scanning or CVE detection

Authentication beyond a GitHub PAT

Readiness Classification Model
Condition	Result
Any CI signal failing	CI_FAILING
CI passing + unresolved actionable review threads	ACTION_REQUIRED
CI passing + no unresolved actionable threads	READY
No CI signals	NO_CI (reported but not READY)

All decisions are deterministic and explainable.

Day-Wise / Step-Wise Execution Plan
Day 1 — PR Ingestion & GitHub API Integration ✅ (Completed)

Steps

Initialize repository with clean module structure

Configure GitHub REST API client using PAT

Implement strict PR URL parser

Fetch PR metadata (title, author, state, commits, files)

Add explicit error handling (invalid URL, private repo, rate limits)

Outcome

CLI accepts PR URL and fetches structured PR metadata

Establishes ingestion layer for downstream analysis

Day 2 — CI Aggregation Engine

Steps

Fetch PR head commit SHA

Retrieve all GitHub Check Runs for the commit

Retrieve all Commit Statuses for the same commit

Normalize CI signals into a unified model

Classify CI state: PASS, FAIL, PENDING, NO_CI

Outcome

Single deterministic CI state derived from all CI providers

Forms first major input to readiness decision

Day 3 — Review Comment & Thread Analysis

Steps

Fetch all PR review comments and threads

Group comments by thread

Identify resolved vs unresolved threads

Ignore comments authored by PR owner

Count unresolved reviewer threads as actionable feedback

Heuristics

Resolved threads → ignored

Unresolved reviewer comments → actionable

No NLP or sentiment inference

Outcome

Clear count of unresolved actionable review feedback

Second core input to readiness decision

Day 4 — Readiness Decision Engine

Steps

Implement deterministic readiness rules

Combine CI state and review analysis

Generate final readiness label

Produce structured explanation for decision

Example Output

{
  "ci_state": "PASS",
  "unresolved_threads": 1,
  "readiness": "ACTION_REQUIRED"
}


Outcome

Transparent, explainable readiness classification

Mirrors intended Project E behavior

Day 5 — CLI Output & UX Stabilization

Steps

Enhance CLI output formatting

Display CI summary, review summary, and final readiness

Add usage instructions and examples

Validate behavior on multiple public PRs

Outcome

Reproducible, demo-ready CLI tool

Easy for mentors to test locally

Day 6 — Edge-Case Handling & Hardening

Steps

Handle PRs with no CI

Handle PRs with no reviews

Improve rate-limit and API failure messaging

Add basic unit tests for core logic

Outcome

Robust behavior across real-world PRs

Reduced mentor intervention risk

Day 7 — Documentation & Proposal Integration

Steps

Document architecture and data flow

Clearly list supported vs unsupported features

Map demo components to full Project E roadmap

Add screenshots or CLI output examples

Prepare proposal-ready explanation

Outcome

Polished prototype suitable for proposal review

Clear upgrade path into full GSoC project

Deliverables Summary

GitHub repository with working prototype

Deterministic PR readiness pipeline

Clear documentation and scope boundaries

Live demo that mentors can reproduce

How This Scales into Full Project E

This mini demo directly evolves into:

Multi-PR dashboard

Reviewer intent classification

Bot-aware analysis (CodeRabbit, Cursor, etc.)

Advisory security triage extension

No rewrite required — only incremental extension.

Why This Plan Is Low-Risk

Deterministic logic first

Human-interpretable outputs

Clear scope discipline

Independent weekly milestones

Final Note (mentor psychology)

This plan demonstrates execution, not aspiration.

That’s exactly what gets selected.