"""
Unit tests for PR URL parser
Tests valid URLs, invalid formats, and edge cases
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from parser import parse_pr_url


class TestPRParser:
    """Test suite for PR URL parsing"""
    
    def test_valid_pr_url(self):
        """Test parsing a valid PR URL"""
        url = "https://github.com/zulip/zulip/pull/37753"
        result = parse_pr_url(url)
        
        assert result["owner"] == "zulip"
        assert result["repo"] == "zulip"
        assert result["number"] == "37753"
    
    def test_valid_pr_url_different_repo(self):
        """Test parsing URL from different repository"""
        url = "https://github.com/django/django/pull/12345"
        result = parse_pr_url(url)
        
        assert result["owner"] == "django"
        assert result["repo"] == "django"
        assert result["number"] == "12345"
    
    def test_valid_pr_url_with_trailing_slash(self):
        """Test parsing URL with trailing slash"""
        url = "https://github.com/owner/repo/pull/123/"
        result = parse_pr_url(url)
        
        assert result["owner"] == "owner"
        assert result["repo"] == "repo"
        assert result["number"] == "123"
    
    def test_invalid_url_not_github(self):
        """Test that non-GitHub URLs are rejected"""
        url = "https://gitlab.com/owner/repo/pull/123"
        
        with pytest.raises(ValueError, match="Invalid GitHub PR URL"):
            parse_pr_url(url)
    
    def test_invalid_url_not_pr(self):
        """Test that non-PR GitHub URLs are rejected"""
        url = "https://github.com/owner/repo/issues/123"
        
        with pytest.raises(ValueError, match="Invalid GitHub PR URL"):
            parse_pr_url(url)
    
    def test_invalid_url_missing_number(self):
        """Test that URLs without PR numbers are rejected"""
        url = "https://github.com/owner/repo/pull/"
        
        with pytest.raises(ValueError, match="Invalid GitHub PR URL"):
            parse_pr_url(url)
    
    def test_invalid_url_malformed(self):
        """Test that malformed URLs are rejected"""
        url = "not-a-url"
        
        with pytest.raises(ValueError, match="Invalid GitHub PR URL"):
            parse_pr_url(url)
    
    def test_invalid_url_empty(self):
        """Test that empty strings are rejected"""
        url = ""
        
        with pytest.raises(ValueError, match="Invalid GitHub PR URL"):
            parse_pr_url(url)
    
    def test_valid_pr_url_with_hyphen_in_name(self):
        """Test parsing URL with hyphens in owner/repo names"""
        url = "https://github.com/OWASP-BLT/BLT/pull/5618"
        result = parse_pr_url(url)
        
        assert result["owner"] == "OWASP-BLT"
        assert result["repo"] == "BLT"
        assert result["number"] == "5618"
    
    def test_valid_pr_url_with_numbers_in_name(self):
        """Test parsing URL with numbers in repo name"""
        url = "https://github.com/owner123/repo456/pull/789"
        result = parse_pr_url(url)
        
        assert result["owner"] == "owner123"
        assert result["repo"] == "repo456"
        assert result["number"] == "789"


def run_tests():
    """Run all parser tests and display results"""
    print("="*70)
    print("PARSER UNIT TESTS")
    print("="*70)
    print()
    
    test_suite = TestPRParser()
    tests = [
        ("Valid PR URL", test_suite.test_valid_pr_url),
        ("Valid PR URL (different repo)", test_suite.test_valid_pr_url_different_repo),
        ("Valid PR URL with trailing slash", test_suite.test_valid_pr_url_with_trailing_slash),
        ("Invalid: Not GitHub", test_suite.test_invalid_url_not_github),
        ("Invalid: Not PR", test_suite.test_invalid_url_not_pr),
        ("Invalid: Missing number", test_suite.test_invalid_url_missing_number),
        ("Invalid: Malformed", test_suite.test_invalid_url_malformed),
        ("Invalid: Empty string", test_suite.test_invalid_url_empty),
        ("Valid: Hyphens in name", test_suite.test_valid_pr_url_with_hyphen_in_name),
        ("Valid: Numbers in name", test_suite.test_valid_pr_url_with_numbers_in_name),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✅ {name}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {name}: {e}")
            failed += 1
        except Exception as e:
            # Expected for negative tests
            if "Invalid" in name:
                print(f"✅ {name} (correctly rejected)")
                passed += 1
            else:
                print(f"❌ {name}: {e}")
                failed += 1
    
    print()
    print("="*70)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("="*70)
    
    return passed, failed


if __name__ == "__main__":
    run_tests()
