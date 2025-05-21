import logging
from datetime import datetime

# Configuration for logging: adjust file path and format as necessary
LOG_FILE_PATH = 'access.log'
LOG_FORMAT = '%(asctime)s - %(user_id)s - %(access_outcome)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, filename=LOG_FILE_PATH, filemode='a')

def log_access_attempt(user_id, access_outcome):
    """
    Records access attempts into a log file.
    
    Args:
    user_id (str): The ID of the user attempting access.
    access_outcome (str): The outcome of the access attempt (e.g., 'success' or 'failure').
    
    Returns:
    None
    """

    # Validate input parameters
    if not isinstance(user_id, str) or not user_id:
        raise ValueError("user_id must be a non-empty string")
    if access_outcome not in ['success', 'failure']:
        raise ValueError("access_outcome must be either 'success' or 'failure'")

    # Create log record
    record = {
        'asctime': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': user_id,
        'access_outcome': access_outcome
    }

    # Log the record
    logging.info(record)

# Example usage:
# log_access_attempt("user123", "success")
# log_access_attempt("user456", "failure")
