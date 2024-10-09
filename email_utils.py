import imaplib
import email
from email.header import decode_header

# Configuration for your email account
IMAP_SERVER = "imap.gmail.com"  # For Gmail
IMAP_PORT = 993
USERNAME = "your_email@gmail.com"  # Replace with your Gmail address
PASSWORD = "your_password"  # Replace with your Gmail app-specific password

def connect_to_inbox():
    """Connects to the email inbox using IMAP."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(USERNAME, PASSWORD)
        mail.select("inbox")  # Select the inbox folder
        return mail
    except Exception as e:
        print(f"Error connecting to inbox: {e}")
        return None

def fetch_emails(mail, num_emails=5):
    """Fetches the most recent emails."""
    try:
        # Search for all emails in the inbox
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()[-num_emails:]  # Get the latest emails
        email_list = []

        for email_id in email_ids:
            res, msg = mail.fetch(email_id, "(RFC822)")
            for response_part in msg:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    from_ = msg.get("From")
                    email_list.append((subject, from_, msg))
        return email_list
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []

def parse_email_body(msg):
    """Parses the body of the email message."""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()
    return ""
