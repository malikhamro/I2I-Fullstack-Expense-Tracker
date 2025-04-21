import json
import os
import datetime
from notifications.notifications_handler import (
    send_email_notification,
    send_sms_notification,
    send_push_notification
)
from config_logger import log_changes

# Function to track changes
def track_changes(changes):
    """
    This function tracks the configuration changes made to the system and calls 
    the appropriate notification functions from notifications_handler.py.
    
    Parameters:
    changes (dict): A dictionary containing the configuration changes.
    Example:
    {
        'hostname': 'new-hostname',
        'ip_address': '192.168.1.1',
        'port': 8080
    }
    """

    # Validate input
    if not isinstance(changes, dict):
        raise ValueError("Changes must be provided as a dictionary")

    # Log the changes
    log_changes(changes)

    # Send notifications
    try:
        send_email_notification(f"Configuration changes detected: {json.dumps(changes, indent=2)}")
        send_sms_notification(f"Configuration changes detected.")
        send_push_notification(f"Configuration changes detected.")
    except Exception as e:
        # Handle any errors that might occur during notification sending
        raise RuntimeError(f"Failed to send notifications due to: {e}")

    print(f"Configuration changes tracked and notifications sent successfully at {datetime.datetime.now()}")

# Sample changes for testing the function
if __name__ == "__main__":
    sample_changes = {
        'hostname': 'new-hostname',
        'ip_address': '192.168.1.1',
        'port': 8080
    }
    try:
        track_changes(sample_changes)
    except Exception as e:
        print(f"Error: {e}")
