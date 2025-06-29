import pytest
from qrscan import url_checker

def test_is_url_suspicious_heuristic():
    assert url_checker.is_url_suspicious_heuristic("http://example.com") is False
    assert url_checker.is_url_suspicious_heuristic("http://badsite.ru") is True 