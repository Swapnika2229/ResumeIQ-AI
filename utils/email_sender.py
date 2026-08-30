import os
import yagmail
from dotenv import load_dotenv

load_dotenv()

sender = os.getenv("EMAIL_ADDRESS")
app_password = os.getenv("EMAIL_PASSWORD")


def send_report(receiver_email, pdf_file):

    yag = yagmail.SMTP(sender, app_password)

    yag.send(
        to=receiver_email,
        subject="ResumeIQ AI Report",
        contents="""
Hello,

Your AI Resume Analysis Report is attached.

Thank you for using ResumeIQ AI.
""",
        attachments=pdf_file
    )