"""Basic website assessment utilities."""

from __future__ import annotations

from typing import Dict, List
from urllib.request import Request, urlopen
from urllib.error import URLError


def assess_website(url: str, timeout: int = 5) -> Dict[str, object]:
    """Run a simple security assessment against a website.

    Parameters
    ----------
    url:
        URL of the website to assess.
    timeout:
        Timeout in seconds for the HTTP request.

    Returns
    -------
    dict
        Dictionary containing the score and detected issues.
    """
    score = 0
    checks = 0
    issues: List[str] = []

    if url.startswith("https://"):
        score += 1
    else:
        issues.append("URL does not use HTTPS.")
    checks += 1

    try:
        req = Request(url, headers={"User-Agent": "CyberAI"})
        with urlopen(req, timeout=timeout) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
    except URLError as exc:  # pragma: no cover - network errors
        issues.append(f"Error fetching URL: {exc}")
        return {"url": url, "score": 0.0, "issues": issues}

    security_headers = [
        "content-security-policy",
        "x-content-type-options",
        "x-frame-options",
        "strict-transport-security",
    ]
    for header in security_headers:
        checks += 1
        if header in headers:
            score += 1
        else:
            issues.append(f"Missing header: {header}")

    score_percent = round(100 * score / checks, 2) if checks else 0.0
    return {"url": url, "score": score_percent, "issues": issues}
