# File: data_consistency/notifications.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

# Constants for email server configuration
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'alert@example.com'
SMTP_PASSWORD = 'yourpassword'

class NotificationsManager:
    def __init__(self, smtp_server=SMTP_SERVER, smtp_port=SMTP_PORT, smtp_username=SMTP_USERNAME, smtp_password=SMTP_PASSWORD):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def send_alert(self, recipient_list: List[str], subject: str, message_body: str) -> None:
        """
        Sends an alert notification if any inconsistencies are detected during monitoring.

        :param recipient_list: List of email recipients
        :param subject: Subject of the email
        :param message_body: Body of the email
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = ', '.join(recipient_list)
            msg['Subject'] = subject

            msg.attach(MIMEText(message_body, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(msg['From'], recipient_list, msg.as_string())
            print(f"Alert sent successfully to {recipient_list}")

        except Exception as e:
            print(f"Failed to send alert: {e}")
            raise

    def notify_policy_update(self, recipient_list: List[str], policy_name: str) -> None:
        """
        Notify relevant stakeholders of any updates to the consistency policies.

        :param recipient_list: List of email recipients
        :param policy_name: Name of the policy that has been updated
        """
        subject = "Data Consistency Policy Update Notification"
        message_body = f"The data consistency policy '{policy_name}' has been updated. Please review the changes."

        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = ', '.join(recipient_list)
            msg['Subject'] = subject

            msg.attach(MIMEText(message_body, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(msg['From'], recipient_list, msg.as_string())
            print(f"Policy update notification sent successfully to {recipient_list}")

        except Exception as e:
            print(f"Failed to send policy update notification: {e}")
            raise

# Example usage
if __name__ == "__main__":
    notifier = NotificationsManager()
    rec_list = ['user1@example.com', 'user2@example.com']
    
    # Send an alert about inconsistencies
    notifier.send_alert(rec_list, "Data Inconsistency Detected", "Inconsistencies have been detected in the system. Immediate action is required.")

    # Send notification about policy update
    notifier.notify_policy_update(rec_list, "Data Consistency Policy v2.0")
