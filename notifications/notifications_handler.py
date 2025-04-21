# notifications/notifications_handler.py

import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration for setting up notifications
ADMIN_EMAIL = 'admin@example.com'
SMS_API_ENDPOINT = 'https://sms-provider.example.com/send'
SMS_API_KEY = 'your-sms-api-key'
PUSH_API_ENDPOINT = 'https://push-provider.example.com/notify'
PUSH_API_KEY = 'your-push-api-key'

def send_email_notification(subject, message):
    """
    This function will send an email notification to the system administrator when a configuration change occurs.
    
    :param subject: Subject of the email
    :param message: Body of the email
    :return: None
    """
    try:
        # Construct the email
        email = MIMEMultipart()
        email['From'] = 'no-reply@example.com'
        email['To'] = ADMIN_EMAIL
        email['Subject'] = subject
        email.attach(MIMEText(message, 'plain'))
        
        # Send the email
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login('your-username', 'your-password')
            server.sendmail(email['From'], email['To'], email.as_string())
        print('Email notification sent successfully.')

    except Exception as e:
        # Handle exceptions for better debugging and alerting
        print(f'Failed to send email notification. Error: {e}')

def send_sms_notification(message):
    """
    This function will send an SMS notification to the system administrator when a configuration change occurs.
    
    :param message: The text message to be sent
    :return: None
    """
    try:
        # Prepare SMS payload
        payload = {
            'api_key': SMS_API_KEY,
            'to': '+1234567890',  # Target phone number
            'message': message,
        }
        
        # Send SMS via API
        response = requests.post(SMS_API_ENDPOINT, json=payload)
        response.raise_for_status()
        print('SMS notification sent successfully.')

    except requests.RequestException as e:
        # Handle exceptions for better debugging and alerting
        print(f'Failed to send SMS notification. Error: {e}')

def send_push_notification(title, message):
    """
    This function will send a push notification to the system administrator when a configuration change occurs.
    
    :param title: Title of the push notification
    :param message: Body of the push notification
    :return: None
    """
    try:
        # Prepare Push notification payload
        payload = {
            'api_key': PUSH_API_KEY,
            'to': 'device-token',  # Replace with actual device token
            'title': title,
            'message': message,
        }
        
        # Send Push notification via API
        response = requests.post(PUSH_API_ENDPOINT, json=payload)
        response.raise_for_status()
        print('Push notification sent successfully.')

    except requests.RequestException as e:
        # Handle exceptions for better debugging and alerting
        print(f'Failed to send push notification. Error: {e}')

