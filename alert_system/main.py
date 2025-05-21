# alert_system/main.py

import sys
import logging
from datetime import datetime
from alert_system.detector.unauthorized_access_detector import detect_unauthorized_access
from alert_system.logger.access_logger import log_access_attempt
from alert_system.alerter.alert_sender import send_alert

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_alert_system():
    """
    This function initializes and starts the alert system.
    """

    try:
        logger.info("Starting alert system...")

        while True:
            # Monitor access logs and detect unauthorized access attempts
            unauthorized_access = detect_unauthorized_access()
            
            if unauthorized_access:
                # Log the access attempt
                log_access_attempt(unauthorized_access)
                
                # Send an alert to the security analyst
                send_alert(unauthorized_access)

    except KeyboardInterrupt:
        logger.info("Alert system terminated by user.")
        sys.exit(0)
    except Exception as e:
        logger.error("An error occurred while running the alert system: %s", str(e))
        sys.exit(1)

if __name__ == "__main__":
    run_alert_system()
