import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from cyberai.assessment import assess_website


def test_assess_website_https_and_headers():
    mock_resp = MagicMock()
    mock_resp.headers = {
        'Content-Security-Policy': 'default-src self',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'Strict-Transport-Security': 'max-age=31536000',
    }
    mock_context = MagicMock()
    mock_context.__enter__.return_value.headers = mock_resp.headers
    with patch('cyberai.assessment.urlopen', return_value=mock_context):
        result = assess_website('https://example.com')
    assert result['score'] == 100.0
    assert result['issues'] == []


def test_assess_website_missing_headers_and_http():
    mock_resp = MagicMock()
    mock_resp.headers = {}
    mock_context = MagicMock()
    mock_context.__enter__.return_value.headers = mock_resp.headers
    with patch('cyberai.assessment.urlopen', return_value=mock_context):
        result = assess_website('http://example.com')
    assert result['score'] < 100.0
    assert 'URL does not use HTTPS.' in result['issues']
