# File: alert_system/detector/unauthorized_access_detector.py

import time
import re
from ..logger.access_logger import log_access_attempt
from ..alerter.alert_sender import send_alert

# Constants for log monitoring
LOG_FILE_PATH = '/var/log/access.log'
UNAUTHORIZED_ACCESS_PATTERN = re.compile(r'UNAUTHORIZED ACCESS')

def detect_unauthorized_access(interval=5):
    """
    Monitors access logs in real-time and detects unauthorized access attempts.
    If an unauthorized attempt is detected, an alert is triggered.

    Args:
        interval (int): The time interval (in seconds) to check the log file for new entries.
    """
    try:
        with open(LOG_FILE_PATH, 'r') as log_file:
            # Move to the end of the file
            log_file.seek(0, 2)
            
            while True:
                line = log_file.readline()
                if not line:
                    time.sleep(interval)
                    continue
                
                log_access_attempt(line)
                
                if UNAUTHORIZED_ACCESS_PATTERN.search(line):
                    # Extract details (Example assumes message contains user ID and timestamp)
                    details = extract_details_from_log(line)
                    send_alert(details)
    except FileNotFoundError:
        print(f"Error: Log file not found at {LOG_FILE_PATH}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def extract_details_from_log(log_line):
    """
    Extracts relevant details from a log line.

    Args:
        log_line (str): The log line containing the access attempt details.

    Returns:
        dict: A dictionary with relevant details extracted from the log line,
              such as user ID and timestamp.
    """
    # For simplicity, assuming log format is: "[timestamp] User 'userID' attempted access: OUTCOME"
    match = re.match(r"\[(.*?)\] User '(.*?)' attempted access: (.*)", log_line)
    if match:
        return {
            'timestamp': match.group(1),
            'user_id': match.group(2),
            'outcome': match.group(3)
        }
    return {}

