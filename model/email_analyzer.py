import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class EmailAnalyzer:
    #Handles email analysis for phishing indicators

    def __init__(self):
        self.suspicious_keywords = ["urgent", "free", "verify", "limited time", "prize","warning","account suspended","security alert","action required"]
        self.suspicious_extensions = [".exe", ".bat", ".scr", ".vbs", ".js", ".pif", ".com", ".lnk"]

    def analyze_email(self, email_body):
        #Analyzes the email body for phishing indicators
        urls = self.extract_urls(email_body)
        for url in urls:
            domain = urlparse(url).netloc
            if self.is_suspicious_domain(domain) or self.check_urlhaus(url):
                return True

        # Check for suspicious keywords
        for keyword in self.suspicious_keywords:
            if keyword.lower() in email_body.lower():
                return True

        return False

    def extract_urls(self, email_body):
        #Extracts URLs from the email body.
        return re.findall(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+', email_body)

    def is_suspicious_domain(self, domain):
        #Check for patterns in domain names that could indicate phishing.
        return "login" in domain or "secure" in domain or "-" in domain

    def check_urlhaus(self, url):
        #Check URL against URLhaus for known phishing URLs.
        try:
            response = requests.get(f"https://urlhaus-api.abuse.ch/v1/url/", data={'url': url})
            if response.status_code == 200:
                result = response.json()
                return result.get("query_status") == "malicious"
        except requests.RequestException as e:
            print(f"Error checking URLhaus: {e}")
        return False
