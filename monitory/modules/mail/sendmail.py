import subprocess
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
import smtplib

def send_alert_email(subject,message,pdf_path):
    try:
        sender = "sender@gmail.com"
        receiver = ["reciber@hotmail.com"]
        email = EmailMessage()
        email["From"] = sender
        email["To"] = ", ".join(receiver) #receiver
        email["Subject"] = subject
        email.set_content(message)

        # Atach PDF
        pdf_file = Path(pdf_path)
        with open(pdf_file, "rb") as f:
            email.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=pdf_file.name
            )

        smtp = smtplib.SMTP_SSL("smtp.gmail.com")
        smtp.login(sender, "<email token or password>")
        smtp.sendmail(sender, receiver, email.as_string())
        smtp.quit()

        print("Email send succesful")

    except Exception as e:
        print(f"Error to send email: {e}")