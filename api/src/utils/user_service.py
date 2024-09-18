import os

from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
load_dotenv('.env')

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_FROM_NAME=os.getenv('MAIN_FROM_NAME'),
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True
)

html_content = """"
<html>
<body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
<div style="width: 100%; background: #efefef; border-radius: 10px; padding: 10px;">
  <div style="margin: 0 auto; width: 90%; text-align: center;">
    <!-- <h1 style="background-color: rgba(0, 53, 102, 1); padding: 5px 10px; border-radius: 5px; color: white;">INDOOR TRACKING</h1> -->
    <div style="margin: 30px auto; background: white; width: 30rem; border-radius: 10px; padding: 50px; text-align: center;">
      
      <img src="cid:logo"  alt="logo" style="width: 15rem"/>
      
      <h3 style="margin-bottom: 20px; font-size: 25px;">Redefinir senha</h3>
     
      <p style="margin-bottom: 10px;">Insira uma nova senha:</p>

      <form method="GET" action="https://www.google.com/search" target="_blank">
        <!-- Campo de entrada de senha -->
        <input id="password" 
               style="width: 200px; font-size: 16px; padding: 10px;" 
               type="password" 
               name="q" 
               placeholder="Digite sua senha">
          
        <!-- Botão de redefinir -->
        <input style="display: block; margin: 0 auto; border: none; background-color: #F1B600; color: #394170; width: 200px; line-height: 24px; padding: 10px; font-size: 24px; border-radius: 10px; cursor: pointer; text-decoration: none;" 
               type="submit" value="Redefinir">
    </form>

    <p>Se você não solicitou essa alteração, ignore este email.</p>

    </div>
  </div>
</div>
</body>
</html>
"""

def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=html_content,
        subtype='html',
        attachments=[{
          "file": "src/utils/assets/logo.png",  # Caminho para a imagem
          "headers": {"Content-ID": "<logo>"}  # Defina o Content-ID para referenciar no HTML
        }]
    )
    fm = FastMail(conf)
    background_tasks.add_task(
       fm.send_message, message)