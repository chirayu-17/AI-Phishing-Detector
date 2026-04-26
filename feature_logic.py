import tldextract
import re

def extract_all_features(url):
    """
    This function takes a raw URL string and returns a list of 5 numbers.
    AI models only understand numbers, not text.
    """
    
    # 1. URL Length: Phishing URLs are often very long to hide the real domain.
    length = len(url)
    
    # 2. Presence of '@': Phishers use '@' to redirect to a different site.
    # 1 if present, 0 if not.
    has_at = 1 if "@" in url else 0
    
    # 3. Dot Count: Phishing sites often have many subdomains (e.g., login.bank.secure.com)
    dots = url.count(".")
    
    # 4. HTTPS Check: Many old phishing sets look for 'https' vs 'http'
    is_https = 1 if url.startswith("https") else 0
    
    # 5. Numerical IP: Does the URL use an IP address instead of a name?
    # Uses a 'Regular Expression' to find patterns like 192.168.1.1
    ip_pattern = r'\d+\.\d+\.\d+\.\d+'
    has_ip = 1 if re.search(ip_pattern, url) else 0
    
    # Return all 5 values as a clean list
    return [length, has_at, dots, is_https, has_ip]