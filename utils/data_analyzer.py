# utils/data_analyzer.py

import logging
import statistics

def analyze_migration_data(migration_data):
    """
    Analyzes migration data to provide insights and updates regarding the progress and current status.
    
    Parameters:
    migration_data (list of dict): List containing migration data records. Each record should be a dictionary with relevant fields.
    
    Returns:
    dict: Analysis insights including progress percentage, average migration speed, estimated time to complete, 
          and any issues or anomalies detected.
    """
    if not migration_data or not isinstance(migration_data, list):
        logging.error("Invalid migration data provided")
        raise ValueError("Migration data must be a non-empty list of dictionaries")

    total_entries = len(migration_data)
    completed_entries = sum(1 for record in migration_data if record.get('status') == 'completed')
    failed_entries = sum(1 for record in migration_data if record.get('status') == 'failed')
    in_progress_entries = sum(1 for record in migration_data if record.get('status') == 'in_progress')

    completion_percentage = (completed_entries / total_entries) * 100 if total_entries > 0 else 0

    # Calculate average migration speed (records per second)
    time_stamps = [record['timestamp'] for record in migration_data if 'timestamp' in record]
    if time_stamps:
        min_time, max_time = min(time_stamps), max(time_stamps)
        total_time = (max_time - min_time).total_seconds()
        avg_migration_speed = total_entries / total_time if total_time > 0 else 0
    else:
        avg_migration_speed = 0

    # Estimate time to complete
    remaining_entries = total_entries - completed_entries
    estimated_time_to_complete = (remaining_entries / avg_migration_speed) if avg_migration_speed > 0 else float('inf')

    # Detect any issues or anomalies
    anomalies = [record for record in migration_data if record.get('anomaly', False)]

    analysis_results = {
        'total_entries': total_entries,
        'completed_entries': completed_entries,
        'failed_entries': failed_entries,
        'in_progress_entries': in_progress_entries,
        'completion_percentage': completion_percentage,
        'average_migration_speed': avg_migration_speed,
        'estimated_time_to_complete': estimated_time_to_complete,
        'anomalies': anomalies,
    }

    logging.info(f"Migration data analysis results: {analysis_results}")
    return analysis_results
