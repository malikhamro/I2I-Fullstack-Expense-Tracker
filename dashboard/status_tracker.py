# dashboard/status_tracker.py

import logging

# Function: initialize_status_tracker
# Description: Sets up mechanisms to monitor the status of each migration task in real-time,
# initializing relevant status flags, and data structures.

def initialize_status_tracker(migration_tasks):
    """
    Initialize the status tracker for monitoring migration tasks.
    
    Args:
    - migration_tasks (list): A list of migration task identifiers.

    Returns:
    - dict: A dictionary with task identifiers as keys and their status flags as values.
    """
    if not isinstance(migration_tasks, list):
        logging.error("Expected a list of migration tasks.")
        raise ValueError("migration_tasks should be a list of task identifiers")

    # Initialize status flags
    status_tracker = {}
    for task in migration_tasks:
        if not isinstance(task, str):
            logging.error(f"Invalid task identifier: {task}. Expected a string.")
            raise ValueError(f"Invalid task identifier: {task}. Expected a string.")
        status_tracker[task] = {
            'status': 'pending',  # Possible values: pending, in-progress, completed, failed
            'last_updated': None  # Timestamp of the last status update
        }

    logging.info(f"Status tracker initialized with {len(migration_tasks)} tasks.")
    return status_tracker

# Example usage
if __name__ == "__main__":
    migration_tasks_example = ["task1", "task2", "task3"]
    try:
        status_tracker = initialize_status_tracker(migration_tasks_example)
        print(status_tracker)
    except ValueError as e:
        print(f"Error initializing status tracker: {e}")
