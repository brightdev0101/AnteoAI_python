import smtplib, ssl

class MailManager:
    '''Simple class to send mail with a standard SMTP mail server
    '''

    def __init__(self):
        self.port = 587
        self.smtp_server = "smtp-relay.sendinblue.com"
        self.sender_email = "alarms@globsit.com"
        self.receiver_email = "gioele5@gmail.com"
        self.password = "VdpjtKFS7gNImAMO"

    def sendRecovery(self, email_recovery):
        context = ssl.create_default_context()
        
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.login(self.sender_email, self.password)
           
            subject = '[Anteo AI] NEW PWD REQUEST'
            content = 'New pwd Request: ' + email_recovery
            message = 'From: {}\nSubject: {}\nTo: {}\n\n{}'.format(self.sender_email, subject, self.receiver_email, content)
            footer = '\n\n\n\n -- \n <b>Anteo AI by Globsit</b>'
            server.sendmail(self.sender_email, self.receiver_email, message + footer)

            server.quit()

    
    def sendMail(self, email_address):    
        context = ssl.create_default_context()
        
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.login(self.sender_email, self.password)
           
            subject = '[Anteo AI] New Subscriber'
            content = 'New subscriber: ' + email_address
            message = 'From: {}\nSubject: {}\nTo: {}\n\n{}'.format(self.sender_email, subject, self.receiver_email, content)
            footer = '\n\n\n\n -- \n <b>Anteo AI by Globsit</b>'
            server.sendmail(self.sender_email, self.receiver_email, message + footer)

            server.quit()
            
    def sendDemo(self, mail, name, company, demo):    
        context = ssl.create_default_context()
        
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.login(self.sender_email, self.password)
           
            subject = '[Anteo AI] Demo Request'
            content = 'New demo request from {} \nName: {} \nCompany:{} \nBrand:{} '.format(mail,name,company,demo)
            message = 'From: {}\nSubject: {}\nTo: {}\n\n{}'.format(self.sender_email, subject, self.receiver_email, content)
            footer = '\n\n\n\n -- \n <b>Anteo AI by Globsit</b>'
            server.sendmail(self.sender_email, self.receiver_email, message + footer)

            server.quit()
            