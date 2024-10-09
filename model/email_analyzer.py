import re
from urllib.parse import urlparse

class EmailAnalyzer:
    #Handles email analysis for phishing indicators

    def __init__(self):
        self.suspicious_keywords = ["urgent", "free", "password", "account", "click here", "verify", "limited time", "prize"]
        self.suspicious_extensions = [".exe", ".bat", ".scr", ".vbs", ".js", ".pif", ".com", ".lnk"]

    def analyze_email(self, email_body):
        #Analyzes the email body for phishing indicators
        # Detect suspicious URLs
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_body)
        for url in urls:
            domain = urlparse(url).netloc
            if self.is_suspicious_domain(domain):
                return True

        # Check for suspicious keywords
        for keyword in self.suspicious_keywords:
            if keyword.lower() in email_body.lower():
                return True

        # Additional checks like file extension can be added if there are attachments
        return False

    def is_suspicious_domain(self, domain):
        #Check for patterns in domain names that could indicate phishing.
        return "login" in domain or "secure" in domain or "-" in domain
