import os
import asyncio
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Template
from datetime import datetime
from zoneinfo import ZoneInfo

from src.database.repositories.user_repository import UserDAO
from src.models.user_model import NotificationBody

from dotenv import load_dotenv
load_dotenv('.env')

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_FROM_NAME="Indoor Tracking",
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True
)

def load_html(file_path: str, context: str) -> str:
    with open(file_path, 'r') as file:
      template = Template(file.read())
      return template.render(context) 
    
def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str):
    context = {
        "email": email_to
    }

    template_path = "src/utils/templates/email_template.html"
    html_content = load_html(template_path,context)

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
    
async def send_mail_notification(subject: str, email_to: str, equipment_name: str, register: str, date: datetime, location: str):
    context = {
        "name": equipment_name,
        "register": register,
        "date": date,
        "location": location
    }

    template_path = "src/utils/templates/email_notification.html"
    html_content = load_html(template_path,context)

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
    asyncio.create_task(fm.send_message(message))
    
async def notify_all_users(notification_body: NotificationBody):
    try: 
    # def notify_all_users():
        userDAO = UserDAO()
        emails = userDAO.get_users_emails()
        
        date_brasilia = notification_body.date.astimezone(ZoneInfo("America/Sao_Paulo"))
        date_key = date_brasilia.strftime("%Y-%m-%d %H:%M:%S")
        # print(emails)
        if emails:
            for email in emails:
                print(email['email'])
                await send_mail_notification('Equipamento mudou de sala', email['email'], notification_body.equipment_name, notification_body.register_, date_key, notification_body.location)
    except Exception as e: 
        print(f"Error sending email: {e}")