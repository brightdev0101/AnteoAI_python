import smtplib, ssl

class MailManager:
    '''Simple class to send mail with a standard SMTP mail server for backup routine
    '''

    def __init__(self):
        self.port = 587
        self.smtp_server = "smtp-relay.sendinblue.com"
        self.sender_email = "alarms@globsit.com"
        self.receiver_email = "consolo@globsit.com"
        self.password = "VdpjtKFS7gNImAMO"


    def sendBackupUpload(self, result):    
        context = ssl.create_default_context()
        
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.login(self.sender_email, self.password)
            
            subject = '[ANTEO AI] Backup Upload Manager'
            content = result
            message = 'From: {}\nSubject: {}\nTo: {}\n\n{}'.format(self.sender_email, subject, self.receiver_email, content)
            footer = '\n\n\n\n -- \n <b>Anteo AI by Globsit</b>'
            server.sendmail(self.sender_email, self.receiver_email, message + footer)

            server.quit()
            