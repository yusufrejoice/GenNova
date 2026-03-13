import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()
def send_welcome_email(to_email, name, role):

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    subject = "Welcome to GenNova"

    body = f"""
Hello {name},

Welcome to GenNova!

Your {role} account has been successfully created.

You can now login and start using AI tools.

Regards,
GenNova Team
"""

    msg = MIMEMultipart()
    msg["From"] = f"GenNova <{smtp_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain", "utf-8"))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_email, smtp_password)

    server.sendmail(smtp_email, to_email, msg.as_string())
    server.quit()