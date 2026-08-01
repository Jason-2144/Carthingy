import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.operations.config import ops_settings

class EmailSender:
    def __init__(self):
        self.host = ops_settings.SMTP_HOST
        self.port = ops_settings.SMTP_PORT
        self.user = ops_settings.SMTP_USER
        self.password = ops_settings.SMTP_PASSWORD
        self.from_email = ops_settings.FROM_EMAIL

    def send_email(self, to_email: str, subject: str, html_content: str):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.from_email
        msg["To"] = to_email

        part = MIMEText(html_content, "html")
        msg.attach(part)

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                if self.user and self.password:
                    server.login(self.user, self.password)
                server.sendmail(self.from_email, to_email, msg.as_string())
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")

email_sender = EmailSender()
