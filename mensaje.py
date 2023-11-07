import os 
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

load_dotenv()

email_sender = "willyalcantara31@gmail.com"
password = os.getenv("PASSWORD")
email_reciver = "willymanuel315@gmail.com"

subject = "Prueba"
body = """
Esta es una prueba para ver si funciona
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_reciver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as stmp:
    stmp.login(email_sender, password)
    stmp.sendmail(email_sender,email_reciver, em.as_string())





