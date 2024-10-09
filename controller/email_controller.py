from model.email_analyzer import EmailAnalyzer
from view.email_inbox_gui import EmailInboxGUI

class EmailController:
    #Controller for handling the inbox and phishing detection

    def __init__(self):
        self.email_analyzer = EmailAnalyzer()
        self.gui = EmailInboxGUI(self.email_analyzer)

    def run(self):
        #Runs the GUI application
        self.gui.mainloop()
