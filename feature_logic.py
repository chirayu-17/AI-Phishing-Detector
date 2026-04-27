import tldextract
import re

def extract_all_features(url):
    # 1. Basics
    length = len(url)
    dots = url.count(".")
    
    # 2. Character Analysis (Phishers love hyphens and special chars)
    hyphens = url.count("-")
    at_symbol = 1 if "@" in url else 0
    
    # 3. Subdomain Depth
    # e.g., "login.bank.secure.com" has 3 parts before the TLD
    extracted = tldextract.extract(url)
    subdomain_count = len(extracted.subdomain.split('.')) if extracted.subdomain else 0
    
    # 4. Suspicious TLD check
    # Many phishing sites use cheap/free domains like .xyz, .tk, .top, .ga
    suspicious_tlds = [".xyz", ".tk", ".top", ".ga", ".ml", ".cf"]
    is_suspicious_tld = 1 if any(tld in url for tld in suspicious_tlds) else 0
    
    # 5. URL Shortener Check
    # Hackers hide links behind bit.ly or tinyurl
    shorteners = ["bit.ly", "goo.gl", "tinyurl", "t.co", "rebrand.ly"]
    is_shortened = 1 if any(s in url for s in shorteners) else 0

    # 6. Protocol
    is_https = 1 if url.startswith("https") else 0

    # Return the NEW list (now 8 features)
    return [length, dots, hyphens, at_symbol, subdomain_count, is_suspicious_tld, is_shortened, is_https]