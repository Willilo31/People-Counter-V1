# import os
# from dotenv import load_dotenv
# from email.message import EmailMessage
# import ssl
# import smtplib

# load_dotenv()

# email_sender = "willyalcantara31@gmail.com"
# password = os.getenv("PASSWORD")
# email_reciver = "john_henry_de_leon@baxter.com"

# subject = "Alerta: Capacidad Máxima en el Departamento"
# body = """
#     <img src="cid:warning.jpeg">
    
#     <br><br> 
    
#     <p>Saludos,</p>

#     <p>Este es un mensaje de alerta para informar que el número de personas en el departamento se está acercando a la capacidad máxima. Actualmente hay <span style="color: red; font-weight: bold;">8</span> personas en el departamento, y la capacidad máxima es de <span style="color: red; font-weight: bold;">10</span> personas.</p>
    
#     <p>Por favor, tome medidas para gestionar la situación.</p>

#     <p>Atentamente,</p>
#     <p>El Sistema de Alerta</p>
#     """
# # Crea un objeto EmailMessage
# em = EmailMessage()
# em['From'] = email_sender
# em['To'] = email_reciver
# em['Subject'] = subject
# em.set_content(body, subtype='html')

# # Adjunta una imagen al correo y la referencia en el cuerpo
# with open("warning.jpeg", "rb") as img_file:
#     img_data = img_file.read()
#     em.add_attachment(img_data, maintype="image", subtype="jpeg", filename="warning.jpeg", cid="warning.jpeg")

# context = ssl.create_default_context()

# with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as stmp:
#     stmp.login(email_sender, password)
#     stmp.sendmail(email_sender, email_reciver, em.as_string())
