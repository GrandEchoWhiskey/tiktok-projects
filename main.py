import re
from urllib.parse import urlparse

# Suspicious keywords often used in phishing URLs
PHISHING_KEYWORDS = [
    "login", "verify", "update", "secure", "account", "bank", "confirm",
    "password", "admin", "support"
]

# Regular expression for detecting IP addresses in URLs
IP_ADDRESS_REGEX = r"^\d{1,3}(\.\d{1,3}){3}$"

# Function to check if a URL contains phishing patterns
def is_phishing_url(url: str) -> bool:
    # Parse the URL
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    # Check if domain is an IP address
    if re.match(IP_ADDRESS_REGEX, domain):
        print("[ALERT] URL uses an IP address instead of a domain.")
        return True

    # Check for suspicious keywords in the URL
    for keyword in PHISHING_KEYWORDS:
        if keyword in domain.lower() or keyword in path.lower():
            print(f"[ALERT] Suspicious keyword '{keyword}' found in the URL.")
            return True

    # Check for multiple subdomains (e.g., phishing.bank.example.com)
    subdomain_count = domain.count(".")
    if subdomain_count > 2:
        print("[ALERT] URL has too many subdomains.")
        return True

    # Check for mismatched top-level domains
    known_domains = [".com", ".org", ".net", ".gov", ".edu"]
    if not any(domain.endswith(tld) for tld in known_domains):
        print("[ALERT] URL uses an uncommon top-level domain.")
        return True

    return False

# Example usage
urls_to_check = [
    "http://192.168.0.1/login",
    "http://secure-login.bank-example.com",
    "http://example.com/update-password",
    "http://my-safe-website.net"
]

for url in urls_to_check:
    print(f"\nChecking URL: {url}")
    if is_phishing_url(url):
        print("Phishing detected!")
    else:
        print("URL seems safe.")