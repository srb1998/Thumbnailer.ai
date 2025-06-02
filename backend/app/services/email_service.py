import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from config import settings

class EmailService:
    def __init__(self):
        self.smtp_server = settings.EMAIL_HOST
        self.smtp_port = settings.EMAIL_PORT
        self.username = settings.EMAIL_USER
        self.password = settings.EMAIL_PASSWORD

    def send_thumbnail_email(self, to_email: str, thumbnail_path: str, title: str) -> bool:
        """Send generated thumbnail via email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = f"Your YouTube Thumbnail: {title}"

            body = f"""
            Hi there!

            Your custom YouTube thumbnail for "{title}" is ready!

            The thumbnail has been generated using AI and optimized for maximum click-through rates.

            Tips for using your thumbnail:
            - Upload it directly to YouTube when publishing your video
            - Test different versions to see what works best
            - Make sure it looks good on mobile devices

            Happy creating!
            
            Best regards,
            YouTube Thumbnail AI Team
            """

            msg.attach(MIMEText(body, 'plain'))

            # Attach thumbnail
            if os.path.exists(thumbnail_path):
                with open(thumbnail_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= thumbnail.jpg'
                    )
                    msg.attach(part)

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.username, to_email, text)
            server.quit()
            return True

        except Exception as e:
            print(f"Email sending failed: {e}")
            return False

    def send_feedback_email(self, user_email: str, feedback: str) -> bool:
        """Send user feedback to admin"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = self.username  # Send to admin
            msg['Subject'] = "User Feedback - YouTube Thumbnail AI"

            body = f"""
            New feedback received:
            
            User Email: {user_email}
            Feedback: {feedback}
            """

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.username, self.username, text)
            server.quit()
            return True

        except Exception as e:
            print(f"Feedback email failed: {e}")
            return False