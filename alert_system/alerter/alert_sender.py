# alert_system/alerter/alert_sender.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_alert(alert_details):
    """
    This function sends an alert to the security analyst when an unauthorized access attempt is detected,
    providing details of the attempt.

    :param alert_details: A dictionary containing details of the unauthorized access attempt.
                          Expected keys: 'timestamp', 'user_id', 'source_ip', 'target_resource', 'action'
    :type alert_details: dict
    """
    try:
        # Validate alert_details
        required_keys = {'timestamp', 'user_id', 'source_ip', 'target_resource', 'action'}
        if not all(key in alert_details for key in required_keys):
            raise ValueError(f"alert_details must contain keys: {required_keys}")

        # Email configuration
        sender_email = "alertsystem@example.com"
        receiver_email = "security@example.com"
        subject = "Unauthorized Access Attempt Detected"
        smtp_server = "smtp.example.com"
        smtp_port = 587
        smtp_username = "smtp_user"
        smtp_password = "smtp_pass"

        # Create the email content
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        body = (
            f"An unauthorized access attempt was detected.\n\n"
            f"Timestamp: {alert_details['timestamp']}\n"
            f"User ID: {alert_details['user_id']}\n"
            f"Source IP: {alert_details['source_ip']}\n"
            f"Target Resource: {alert_details['target_resource']}\n"
            f"Action: {alert_details['action']}\n"
        )
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_username, smtp_password)
            server.send_message(message)

        logger.info("Alert sent successfully.")

    except Exception as e:
        logger.error(f"Failed to send alert: {e}")
        raise

