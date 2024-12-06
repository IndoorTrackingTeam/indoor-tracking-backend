from unittest.mock import Mock, AsyncMock, patch
from fastapi import BackgroundTasks
from src.utils.user_service import send_email_background, send_mail_notification, notify_all_users
from datetime import datetime
import pytest 
from src.models.user_model import NotificationBody

import os

def test_load_html_file_exists():
    # Simula o caminho do template para teste
    template_path = "src/utils/templates/email_template.html"

    # Verifica se o arquivo existe
    assert os.path.exists(template_path), f"The template file {template_path} does not exist."
    
def test_send_email_background():
    background_tasks = BackgroundTasks()
    mock_add_task = Mock()
    background_tasks.add_task = mock_add_task

    subject = "Test Subject"
    email_to = "test@example.com"

    send_email_background(background_tasks, subject, email_to)

    mock_add_task.assert_called_once()

@patch("src.utils.user_service.FastMail")
@pytest.mark.asyncio
async def test_send_mail_notification(mock_fastmail):
    mock_send_message = AsyncMock()
    mock_fastmail.return_value.send_message = mock_send_message

    subject = "Test Notification"
    email_to = "test@example.com"
    equipment_name = "Equipment 1"
    register = "123456"
    date = datetime.now()
    location = "Room 101"

    await send_mail_notification(subject, email_to, equipment_name, register, date, location)

    mock_send_message.assert_called_once()

@patch("src.utils.user_service.UserDAO")
@patch("src.utils.user_service.send_mail_notification")
@pytest.mark.asyncio
async def test_notify_all_users(mock_send_mail, mock_userdao):
    mock_userdao.return_value.get_users_emails.return_value = [
        {"email": "user1@example.com"},
        {"email": "user2@example.com"}
    ]
    mock_send_mail.return_value = AsyncMock()

    notification_body = NotificationBody(
        equipment_name="Equipment A",
        register_="123456",
        date=datetime.now(),
        location="Emergency"
    )

    await notify_all_users(notification_body)

    assert mock_send_mail.call_count == 2

@patch("src.utils.user_service.UserDAO")
@patch("src.utils.user_service.send_mail_notification")
@pytest.mark.asyncio
async def test_notify_all_users_no_email_found(mock_send_mail, mock_userdao):
    mock_userdao.return_value.get_users_emails.return_value = []
    mock_send_mail.return_value = AsyncMock()

    notification_body = NotificationBody(
        equipment_name="Equipment A",
        register_="123456",
        date=datetime.now(),
        location="Emergency"
    )

    await notify_all_users(notification_body)

    assert mock_send_mail.call_count == 0