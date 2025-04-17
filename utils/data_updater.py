# utils/data_updater.py

import logging
from typing import Any, Dict
from utils.data_analyzer import analyze_migration_data
from utils.data_fetcher import fetch_migration_data

logging.basicConfig(level=logging.INFO)

def update_dashboard_data(dashboard: Any, migration_source: Dict[str, Any]) -> None:
    """
    Updates the dashboard with new data fetched and analyzed for real-time tracking.
    
    Args:
        dashboard (Any): The dashboard instance which needs to be updated.
        migration_source (Dict[str, Any]): Configuration for data fetching from the migration source.
        
    Raises:
        ValueError: If the dashboard or migration_source is None.
        ConnectionError: If there's a failure fetching data from the migration source.
        RuntimeError: If there's an error analyzing the fetched data.
    """
    if dashboard is None or migration_source is None:
        logging.error("Invalid parameters: dashboard and migration_source must be provided.")
        raise ValueError("dashboard and migration_source must be provided.")

    try:
        logging.info("Fetching migration data from source.")
        migration_data = fetch_migration_data(migration_source)
    except ConnectionError as e:
        logging.error(f"Failed to fetch migration data: {e}")
        raise

    try:
        logging.info("Analyzing fetched migration data.")
        analyzed_data = analyze_migration_data(migration_data)
    except Exception as e:
        logging.error(f"Error analyzing migration data: {e}")
        raise RuntimeError(f"Error analyzing migration data: {e}")

    try:
        logging.info("Updating the dashboard with analyzed data.")
        # Assume the dashboard has an update_data method
        dashboard.update_data(analyzed_data)
    except AttributeError as e:
        logging.error(f"Failed to update the dashboard: {e}")
        raise

    logging.info("Dashboard successfully updated with new migration data.")
