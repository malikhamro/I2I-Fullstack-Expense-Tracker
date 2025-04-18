# notifications/change_notifier.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_notification(change_details):
    """
    This function takes the details of the configuration changes as inputs and sends out
    notifications to the system administrator. The function formats the change details
    into a readable message before sending the notification.

    :param change_details: A dictionary containing details about the configuration changes.
    """
    try:
        # Validate change_details
        if not isinstance(change_details, dict):
            raise ValueError("change_details must be a dictionary")

        if 'recipient_email' not in change_details or 'changes' not in change_details:
            raise ValueError("change_details must include 'recipient_email' and 'changes' keys")

        recipient_email = change_details['recipient_email']
        changes = change_details['changes']

        # Format the message
        subject = "Configuration Change Notification"
        body = "The following configuration changes have been detected:\n\n"

        for key, value in changes.items():
            body += f"{key}: {value}\n"

        # Email content setup
        msg = MIMEMultipart()
        msg['From'] = "noreply@system.com"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server = smtplib.SMTP('smtp.mailtrap.io', 587)
        server.starttls()
        server.login('your_smtp_username', 'your_smtp_password')
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

        print(f"Notification sent to {recipient_email}")

    except Exception as e:
        print(f"Failed to send notification: {str(e)}")
        raise

if __name__ == "__main__":
    # Sample change details for testing purposes
    change_details = {
        "recipient_email": "admin@system.com",
        "changes": {
            "config_param_1": "old_value_1 -> new_value_1",
            "config_param_2": "old_value_2 -> new_value_2"
        }
    }
    send_notification(change_details)
