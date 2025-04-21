import logging
from datetime import datetime

# Setup a logger
logger = logging.getLogger('config_changes_logger')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('config_changes.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def log_changes(change_details):
    """Log the configuration changes to a file or database for audit purposes.
    
    Args:
        change_details (dict): Dictionary containing details about the configuration change.
            Expected keys:
                - change_type: str, Type of change (e.g., 'update', 'delete', 'add').
                - changed_by: str, Username of the person who made the change.
                - change_time: datetime, Time when the change was made.
                - change_description: str, Description of the change.
                - previous_value: str, Previous value before the change (optional).
                - new_value: str, New value after the change (optional).
    
    Raises:
        ValueError: If required keys are missing from change_details.
    """
    
    required_keys = ['change_type', 'changed_by', 'change_time', 'change_description']
    
    # Validate the presence of required keys in the change_details
    for key in required_keys:
        if key not in change_details:
            raise ValueError(f"Missing required key: '{key}' in change_details.")
    
    # Ensure change_time is of type datetime
    if not isinstance(change_details['change_time'], datetime):
        raise ValueError(f"The 'change_time' must be a datetime object.")

    # Prepare log entry
    log_entry = (
        f"Change Type: {change_details['change_type']}, "
        f"Changed By: {change_details['changed_by']}, "
        f"Change Time: {change_details['change_time'].strftime('%Y-%m-%d %H:%M:%S')}, "
        f"Description: {change_details['change_description']}"
    )

    # Include previous and new values if they are present
    if 'previous_value' in change_details:
        log_entry += f", Previous Value: {change_details['previous_value']}"
    
    if 'new_value' in change_details:
        log_entry += f", New Value: {change_details['new_value']}"
    
    # Log the change
    logger.info(log_entry)
    
    # Additional logging to database can be implemented here if required


# Example use case
if __name__ == "__main__":
    # Example change details dictionary
    example_change_details = {
        'change_type': 'update',
        'changed_by': 'admin',
        'change_time': datetime.now(),
        'change_description': 'Updated the system configuration for maximum connections.',
        'previous_value': '100',
        'new_value': '150'
    }

    log_changes(example_change_details)

