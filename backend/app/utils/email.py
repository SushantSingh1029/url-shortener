import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.example.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "user@example.com")
SMTP_PASS = os.getenv("SMTP_PASS", "password")

def send_email(to_email: str, subject: str, body: str):
    print("\n" + "=" * 60)
    print("MOCK EMAIL")
    print(f"To      : {to_email}")
    print(f"Subject : {subject}")
    print(f"Body    : {body}")
    print("=" * 60 + "\n")

    # Uncomment below when using a real SMTP server
    # try:
    #     msg = MIMEMultipart()
    #     msg["From"] = SMTP_USER
    #     msg["To"] = to_email
    #     msg["Subject"] = subject
    #     msg.attach(MIMEText(body, "html"))
    #
    #     server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    #     server.starttls()
    #     server.login(SMTP_USER, SMTP_PASS)
    #     server.send_message(msg)
    #     server.quit()
    # except Exception as e:
    #     print(e)