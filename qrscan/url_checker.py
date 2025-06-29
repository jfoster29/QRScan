"""
url_checker.py

Provides URL safety checking using VirusTotal API and heuristics.
"""

from typing import Tuple
import requests
import re
from urllib.parse import urlparse, unquote


def check_url_virustotal(url: str, api_key: str) -> Tuple[bool, str]:
    """
    Check if a URL is malicious using the VirusTotal API.

    Args:
        url: The URL to check.
        api_key: VirusTotal API key.

    Returns:
        Tuple (malicious: bool, source: str), where source is 'VirusTotal' or 'Error'.
    """
    api_url = "https://www.virustotal.com/api/v3/urls"
    headers = {"x-apikey": api_key}
    try:
        resp = requests.post(api_url, headers=headers, data={"url": url}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        malicious_count = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("malicious", 0)
        return malicious_count > 0, "VirusTotal"
    except Exception:
        return False, "Error"


def is_url_suspicious_heuristic(url: str) -> bool:
    """
    Check if a URL is suspicious using basic heuristics.

    Args:
        url: The URL to check.

    Returns:
        True if the URL is suspicious, False otherwise.
    """
    # Suspicious TLDs
    suspicious_tlds = {".ru", ".cn", ".tk", ".ml", ".ga", ".cf", ".gq"}
    
    # Risky keywords
    risky_keywords = ["login", "signin", "password", "bank", "paypal", "bitcoin"]
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Check for suspicious TLDs
        if any(tld in domain for tld in suspicious_tlds):
            return True
            
        # Check for IP-based domains
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain):
            return True
            
        # Check for risky keywords
        if any(keyword in url.lower() for keyword in risky_keywords):
            return True
            
        # Check for percent-encoding
        if "%" in url and len(url) > 100:
            return True
            
        # Check for very long URLs
        if len(url) > 200:
            return True
            
        return False
    except Exception:
        return True 