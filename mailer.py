import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from pathlib import Path


class Mailer:
    def __init__(self, sender_name: str, sender_email: str, api_password: str):
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.api_password = api_password
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 465
        self.smtp_instance: smtplib.SMTP_SSL = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        self.smtp_instance.connect(self.smtp_server, self.smtp_port)
        self.smtp_instance.login(self.sender_email, self.api_password)

    def close_smtp(self):
        self.smtp_instance.quit()

    def send_email(self, recipients: list[str], subject: str, message: str, attachments: list[str]):
        email = MIMEMultipart()
        email['From'] = f"{self.sender_name} <{self.sender_email}>"
        email['To'] = ', '.join(recipients)
        email['Date'] = formatdate(localtime=True)
        email['Subject'] = subject
        email.attach(MIMEText(message, "html"))

        for attachment in attachments:
            part = MIMEBase('application', 'octet-stream')
            with open(attachment, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename={}'.format(Path(attachment).name))
            email.attach(part)

        self.smtp_instance.sendmail(self.sender_email, recipients, email.as_string())
