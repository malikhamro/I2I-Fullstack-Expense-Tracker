# backup_service/logger.py

import logging
from datetime import datetime

# Define the logger and its configuration
logger = logging.getLogger('backup_service_logger')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('backup_service.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_backup_activity(activity, data_size=None, status='Success'):
    """
    Logs all the activities related to the backup process.

    :param activity: Description of the backup activity.
    :param data_size: Size of the data backed up. Optional.
    :param status: Status of the backup operation. Defaults to 'Success'.
    """
    try:
        if not activity:
            raise ValueError("Activity description cannot be empty.")
        
        log_message = f"Backup Activity: {activity}, Status: {status}"
        if data_size is not None:
            log_message += f", Data Size: {data_size} bytes"
        
        logger.info(log_message)
    except Exception as e:
        logger.error(f"Failed to log backup activity: {str(e)}")
        raise

def log_recovery_activity(activity, status='Success', error_message=None):
    """
    Logs all the activities related to the recovery process.

    :param activity: Description of the recovery activity.
    :param status: Status of the recovery operation. Defaults to 'Success'.
    :param error_message: Error message if the recovery operation failed. Optional.
    """
    try:
        if not activity:
            raise ValueError("Activity description cannot be empty.")
        
        log_message = f"Recovery Activity: {activity}, Status: {status}"
        if error_message is not None:
            log_message += f", Error: {error_message}"
        
        logger.info(log_message)
    except Exception as e:
        logger.error(f"Failed to log recovery activity: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    log_backup_activity("Performed daily backup", data_size=1024*1024)
    log_recovery_activity("Initiated recovery from backup", status="Failed", error_message="Backup file not found")
