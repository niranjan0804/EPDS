import tkinter as tk
from tkinter import ttk, messagebox
from email_utils import connect_to_inbox, fetch_emails, parse_email_body

class EmailInboxGUI(tk.Tk):
    """GUI to display emails and detect phishing."""

    def __init__(self, email_analyzer):
        super().__init__()
        self.title("Inbox Email Phishing Detection")
        self.email_analyzer = email_analyzer

        # Fetch Emails Button
        fetch_button = ttk.Button(self, text="Fetch Emails", command=self.fetch_emails)
        fetch_button.grid(row=0, column=0, padx=10, pady=10)

        # Email List
        self.email_listbox = tk.Listbox(self, height=10, width=80)
        self.email_listbox.grid(row=1, column=0, padx=10, pady=10)

        # Display Email Content Button
        display_button = ttk.Button(self, text="Analyze Selected Email", command=self.analyze_email)
        display_button.grid(row=2, column=0, padx=10, pady=10)

        # Email Content Text Area
        self.email_content = tk.Text(self, height=10, width=80)
        self.email_content.grid(row=3, column=0, padx=10, pady=10)

        self.email_data = []  # To store fetched emails

    def fetch_emails(self):
        """Fetches emails from the inbox."""
        mail = connect_to_inbox()  # Connect using utility function
        if mail:
            emails = fetch_emails(mail)
            self.email_listbox.delete(0, tk.END)
            self.email_data = emails
            for idx, (subject, from_, _) in enumerate(emails):
                self.email_listbox.insert(idx, f"From: {from_} | Subject: {subject}")
            mail.logout()

    def analyze_email(self):
        """Analyzes the selected email for phishing."""
        selected_idx = self.email_listbox.curselection()
        if selected_idx:
            email = self.email_data[selected_idx[0]]
            email_body = parse_email_body(email[2])  # Parse using utility function
            self.email_content.delete("1.0", tk.END)
            self.email_content.insert(tk.END, email_body)
            if self.email_analyzer.analyze_email(email_body):
                messagebox.showwarning("Phishing Alert", "This email may be a phishing attempt!")
