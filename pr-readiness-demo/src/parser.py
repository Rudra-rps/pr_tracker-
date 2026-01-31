import re

PR_REGEX = re.compile(
    r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<number>\d+)"
)

def parse_pr_url(url: str):
    match = PR_REGEX.match(url.strip())
    if not match:
        raise ValueError("Invalid GitHub PR URL")
    return match.groupdict()
