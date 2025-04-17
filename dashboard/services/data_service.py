# dashboard/services/data_service.py

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# Simulated database data for the sake of this example
DATABASE = {
    'migration_data': [
        {'id': 1, 'name': 'User1', 'status': 'Complete', 'details': 'Migration successful'},
        {'id': 2, 'name': 'User2', 'status': 'Pending', 'details': 'Migration pending'},
        # Add more mock records as needed
    ]
}

def fetch_migration_data() -> List[Dict[str, Any]]:
    """
    This function retrieves the current data regarding the migration process from the database or other data source.
    """
    try:
        # Add logic to fetch data from an actual database
        migration_data = DATABASE.get('migration_data', [])
        if not migration_data:
            logger.warning("No migration data found")
        return migration_data
    except Exception as e:
        logger.error(f"Error fetching migration data: {e}")
        raise

def aggregate_migration_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    This function processes and aggregates the raw migration data for a summarized view on the dashboard.
    """
    try:
        if not data:
            logger.warning("No data provided for aggregation")
            return {}

        summary = {
            'total_migrations': len(data),
            'completed': sum(1 for item in data if item.get('status') == 'Complete'),
            'pending': sum(1 for item in data if item.get('status') == 'Pending'),
            'failed': sum(1 for item in data if item.get('status') == 'Failed')
        }
        
        logger.debug(f"Aggregated data summary: {summary}")
        return summary
    except Exception as e:
        logger.error(f"Error aggregating migration data: {e}")
        raise
