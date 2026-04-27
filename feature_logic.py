import tldextract
import re

def extract_all_features(url):
    """
    Turns a URL string into a list of 10 numerical features for the AI.
    """
    url = str(url).lower()
    
    # 1. Basic Metadata
    length = len(url)
    dots = url.count(".")
    hyphens = url.count("-")
    at_symbol = 1 if "@" in url else 0
    
    # 2. Subdomain Depth
    extracted = tldextract.extract(url)
    subdomain_count = len(extracted.subdomain.split('.')) if extracted.subdomain else 0
    
    # 3. Protocol Check
    is_https = 1 if url.startswith("https") else 0
    
    # 4. Suspicious TLD check (.xyz, .tk, .ml, etc.)
    suspicious_tlds = [".xyz", ".tk", ".top", ".ga", ".ml", ".cf", ".icu", ".work"]
    is_suspicious_tld = 1 if any(tld in url for tld in suspicious_tlds) else 0
    
    # 5. URL Shortener Check (bit.ly, tinyurl, etc.)
    shorteners = ["bit.ly", "goo.gl", "tinyurl", "t.co", "rebrand.ly", "is.gd"]
    is_shortened = 1 if any(s in url for s in shorteners) else 0

    # 6. NEW: Tunneling Service Detection (Catches Kali/Zphisher links)
    tunneling_services = [
        "trycloudflare.com", 
        "ngrok.io", 
        "ngrok-free.app", 
        "localtunnel.me", 
        "serveo.net"
    ]
    is_tunneled = 1 if any(service in url for service in tunneling_services) else 0

    # 7. NEW: Keyword Brand Analysis
    # Checks for 'high-risk' words often found in phishing subdomains
    keywords = ['login', 'verify', 'secure', 'auth', 'bank', 'account', 'update', 'signin']
    has_keyword = 1 if any(word in url for word in keywords) else 0

    # MUST RETURN ALL 10 FEATURES IN ORDER
    return [
        length, dots, hyphens, at_symbol, 
        subdomain_count, is_https, is_suspicious_tld, 
        is_shortened, is_tunneled, has_keyword
    ]