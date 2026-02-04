"""
Demo script showing expected CLI output format with mock data
This demonstrates the Day 4 confidence scoring engine output
"""

print("="*60)
print("DEMO: CI CONFIDENCE SCORING ENGINE OUTPUT")
print("="*60)
print()

print("PR METADATA")
print("-----------")
print("Title: Add user authentication feature")
print("Author: developer123")
print("State: open")
print("Commits: 8")
print("Changed files: 12")
print()

print("CI STATUS")
print("---------")
print("Unified CI State: PASS")
print("Signals found: 5")
print()

print("="*60)
print("CI RELIABILITY & CONFIDENCE ANALYSIS")
print("="*60)
print("Analyzing historical CI patterns with confidence scoring...")
print()

# Example 1: Reliable check
print("✅ Check: pytest-unit-tests")
print("   Current Status: PASS")
print("   Confidence Score: 100/100")
print("   Classification: RELIABLE")
print("   History: 15 runs (15 pass, 0 fail, 100.0% pass rate)")
print("   Recent Trend: 15 consecutive passes")
print("   Analysis: Perfect track record: 15 consecutive passes with no failures")
print()

# Example 2: Stable check
print("🟢 Check: eslint-code-quality")
print("   Current Status: PASS")
print("   Confidence Score: 80/100")
print("   Classification: STABLE")
print("   History: 12 runs (10 pass, 2 fail, 83.3% pass rate)")
print("   Recent Trend: 5 consecutive passes")
print("   Analysis: Recently stable: 5 consecutive passes (overall 83.3% pass rate)")
print()

# Example 3: Flaky check
print("⚠️  Check: integration-tests-firefox")
print("   Current Status: PASS")
print("   Confidence Score: 35/100")
print("   Classification: FLAKY")
print("   History: 10 runs (6 pass, 4 fail, 60.0% pass rate)")
print("   Recent Trend: 1 consecutive passes")
print("   Analysis: Inconsistent behavior: 5 pass/fail transitions detected across 10 runs")
print()

# Example 4: Unstable check
print("❌ Check: e2e-tests-staging")
print("   Current Status: FAIL")
print("   Confidence Score: 18/100")
print("   Classification: UNSTABLE")
print("   History: 8 runs (2 pass, 6 fail, 25.0% pass rate)")
print("   Recent Trend: 3 consecutive failures")
print("   Analysis: Failing consistently: 3 consecutive failures")
print()

# Example 5: Unknown
print("❔ Check: security-scan")
print("   Current Status: PASS")
print("   Confidence Score: 50/100")
print("   Classification: UNKNOWN")
print("   History: 2 runs (2 pass, 0 fail, 100.0% pass rate)")
print("   Analysis: Insufficient data: Only 2 run(s) available")
print()

print("-" * 60)
print("SUMMARY")
print("-" * 60)
print("Total Checks: 5")
print("  ✅ Reliable: 1")
print("  🟢 Stable: 1")
print("  ⚠️  Flaky: 1")
print("  ❌ Unstable: 1")
print("  ❔ Unknown: 1")
print()
print("⚠️  WARNING: Some CI checks show reliability concerns")
print()
print("="*60)
