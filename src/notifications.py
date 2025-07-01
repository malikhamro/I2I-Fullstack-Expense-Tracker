# src/notifications.py

def notify_stakeholders(claim_details, new_status, remarks=None):
    """
    Sends out notifications to all relevant stakeholders about the status update of a claim.

    Parameters:
    - claim_details (dict): Contains all pertinent information about the claim, including claim ID and current status.
    - new_status (str): The new status to update for the claim.
    - remarks (str, optional): Additional remarks regarding the status update.

    Returns:
    None

    Raises:
    - ValueError: If claim_details or new_status are not provided or invalid.
    - NotificationError: Custom exception if notification process fails
    """
    if not claim_details or 'id' not in claim_details:
        raise ValueError("Invalid claim details provided.")

    if not new_status:
        raise ValueError("New status must be provided.")

    try:
        # Construct the message for the stakeholders
        message = (
            f"Claim ID: {claim_details['id']} status has been updated to {new_status}. "
            f"Current Details: {claim_details}. "
        )
        if remarks:
            message += f"Remarks: {remarks}"

        # Mocking the process of sending notifications
        print(f"Sending notification to stakeholders: {message}")

        # Here, integrate with the actual notification API/service (e.g., email, SMS)
        # send_email(stakeholders_list, message)
        # send_sms(stakeholders_list, message)

    except Exception as e:
        # Logging can be added here
        print(f"Error sending notification: {str(e)}")
        raise NotificationError(f"Failed to send notifications for claim ID: {claim_details['id']}")

class NotificationError(Exception):
    """Custom exception class for notification errors."""
    pass
