import logging
from typing import List, Dict, Any

# Initialize the logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ConsistencyChecker:
    def __init__(self, services_data: List[Dict[str, Any]]):
        """
        Initialize the ConsistencyChecker with data from various microservices.

        :param services_data: List containing data from different microservices
        """
        self.services_data = services_data
        self.inconsistencies = []

    def check_consistency(self) -> bool:
        """
        Compare data across different microservices' databases to ensure consistency.

        :return: Boolean indicating whether or not inconsistencies were found.
        """
        logger.info("Starting consistency check...")
        try:
            reference_data = self.services_data[0]  # Assume the first service data as reference

            for service_data in self.services_data[1:]:
                if service_data != reference_data:
                    logger.warning(f"Inconsistency found: {service_data} does not match {reference_data}")
                    self.inconsistencies.append(service_data)
            
            if self.inconsistencies:
                logger.info("Consistency check completed: Inconsistencies found.")
                return False
            
            logger.info("Consistency check completed: No inconsistencies found.")
            return True
        
        except Exception as e:
            logger.error(f"Error during consistency check: {e}")
            return False

    def log_inconsistencies(self):
        """
        Log any identified inconsistencies for further analysis and reconciliation.
        """
        if not self.inconsistencies:
            logger.info("No inconsistencies to log.")
            return
        
        logger.info("Logging inconsistencies...")
        try:
            for inconsistency in self.inconsistencies:
                logger.error(f"Inconsistency detected: {inconsistency}")

            logger.info("Inconsistencies logged successfully.")
        
        except Exception as e:
            logger.error(f"Error logging inconsistencies: {e}")

    def generate_consistency_report(self) -> Dict[str, Any]:
        """
        Generate a report on the data consistency status across microservices.
        
        :return: Report as a dictionary
        """
        logger.info("Generating consistency report...")
        try:
            report = {
                "total_services": len(self.services_data),
                "inconsistencies_found": len(self.inconsistencies),
                "inconsistency_details": self.inconsistencies,
                "status": "inconsistent" if self.inconsistencies else "consistent"
            }

            logger.info("Consistency report generated successfully.")
            return report
        
        except Exception as e:
            logger.error(f"Error generating consistency report: {e}")
            return {"status": "error", "error_message": str(e)}


# Example usage:
if __name__ == "__main__":
    # Example data from microservices
    data_from_services = [
        {"data": "ABC", "version": 1},
        {"data": "ABC", "version": 1},
        {"data": "XYZ", "version": 2},  # Inconsistent entry
    ]

    checker = ConsistencyChecker(data_from_services)
    if not checker.check_consistency():
        checker.log_inconsistencies()
    
    report = checker.generate_consistency_report()
    logger.info(f"Consistency Report: {report}")
