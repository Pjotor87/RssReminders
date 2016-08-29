#!/usr/bin/env python
import smtplib
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import ApplicationSettings

class Email:
    SenderUsername=''
    SenderPassword=''
    Receiver=''
    Subject=''
    Message=''
    TextTypeIsPlainNotHtml=False
    CompiledMessage=''
    Attachments=[]
    def __init__(self, senderUsername, senderPassword, receiver, subject, message, textTypeIsPlainNotHtml, attachments_list):
        self.SenderUsername = senderUsername
        self.SenderPassword = senderPassword
        self.Receiver = receiver
        self.Subject = subject
        self.Message = message
        self.CompiledMessage = MIMEMultipart('related')
        self.TextTypeIsPlainNotHtml = textTypeIsPlainNotHtml
        self.Attachments = attachments_list
    def send_using_gmail(self):
        self.CompiledMessage['Subject'] = self.Subject
        self.CompiledMessage['From'] = self.SenderUsername
        self.CompiledMessage['To'] = self.Receiver
        self.CompiledMessage.preamble = 'This is a multipart message in MIME format'
        CompiledMessageAlternative = MIMEMultipart('alternative')
        self.CompiledMessage.attach(CompiledMessageAlternative)
        msgText = MIMEText(self.Message, 'plain' if self.TextTypeIsPlainNotHtml else 'html')
        CompiledMessageAlternative.attach(msgText)
        if self.Attachments and len(self.Attachments) > 0:
            for i,attachment in enumerate(self.Attachments):
                try:
                    text = MIMEText('<p>'+os.path.basename(attachment)+'</p><img src="cid:image'+str(i)+'" />', 'html')
                    CompiledMessageAlternative.attach(text)
                    fp = open(attachment, 'rb')
                    img = MIMEImage(fp.read())
                    fp.close()
                    img.add_header('Content-ID', '<image'+str(i)+'>')
                    self.CompiledMessage.attach(img)
                except:
                    print("Unable to open one of the attachments. Error: " + str(sys.exc_info()[0]))
        smtpServer = smtplib.SMTP('smtp.gmail.com', 587)
        smtpServer.starttls()
        smtpServer.login(self.SenderUsername, self.SenderPassword)
        smtpServer.sendmail(self.SenderUsername, self.Receiver, self.CompiledMessage.as_string())
        smtpServer.quit()

def send_gmail_message_from_robot(receiver, subject, message, textTypeIsPlainNotHtml, attachments_list):
    robomail = Email(
        ApplicationSettings.settings.Get("RobotGmailUsername"), 
        ApplicationSettings.settings.Get("RobotGmailPassword"), 
        receiver, 
        subject, 
        message, 
        textTypeIsPlainNotHtml, 
        attachments_list)
    robomail.send_using_gmail();
