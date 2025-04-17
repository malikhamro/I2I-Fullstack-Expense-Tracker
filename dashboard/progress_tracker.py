# dashboard/progress_tracker.py

def initialize_progress_tracker():
    """
    Sets up mechanisms to track the progress of the migration in real-time. 
    Initializes relevant variables and data structures.
    
    Returns:
        dict: A dictionary containing initialized progress tracking structures.
    """
    try:
        progress_tracker = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'pending_tasks': 0,
            'failed_tasks': 0,
            'progress_percentage': 0.0,
            'task_details': []
        }
        
        return progress_tracker
    except Exception as e:
        raise Exception(f"Failed to initialize progress tracker: {str(e)}")


def update_progress_tracker(progress_tracker, task_status, task_id):
    """
    Updates the progress tracker based on the status of a particular task.
    
    Args:
        progress_tracker (dict): The progress tracker dictionary.
        task_status (str): The status of the task ('completed', 'failed', 'pending').
        task_id (str): The identifier of the task being updated.
    
    Returns:
        dict: Updated progress tracker dictionary.
    """
    try:
        if task_status not in ['completed', 'failed', 'pending']:
            raise ValueError("Invalid task status")

        task_found = False
        for task in progress_tracker['task_details']:
            if task['task_id'] == task_id:
                task['status'] = task_status
                task_found = True
                break
        
        if not task_found:
            progress_tracker['task_details'].append({
                'task_id': task_id,
                'status': task_status
            })
        
        progress_tracker['total_tasks'] = len(progress_tracker['task_details'])
        progress_tracker['completed_tasks'] = sum(1 for task in progress_tracker['task_details'] if task['status'] == 'completed')
        progress_tracker['failed_tasks'] = sum(1 for task in progress_tracker['task_details'] if task['status'] == 'failed')
        progress_tracker['pending_tasks'] = sum(1 for task in progress_tracker['task_details'] if task['status'] == 'pending')
        progress_tracker['progress_percentage'] = (progress_tracker['completed_tasks'] / progress_tracker['total_tasks']) * 100 if progress_tracker['total_tasks'] > 0 else 0.0
        
        return progress_tracker
    except Exception as e:
        raise Exception(f"Failed to update progress tracker: {str(e)}")


def get_progress_summary(progress_tracker):
    """
    Provides a summary of the progress tracked.
    
    Args:
        progress_tracker (dict): The progress tracker dictionary.
    
    Returns:
        dict: A summary of the tracking progress.
    """
    try:
        summary = {
            'total_tasks': progress_tracker['total_tasks'],
            'completed_tasks': progress_tracker['completed_tasks'],
            'failed_tasks': progress_tracker['failed_tasks'],
            'pending_tasks': progress_tracker['pending_tasks'],
            'progress_percentage': progress_tracker['progress_percentage']
        }
        
        return summary
    except Exception as e:
        raise Exception(f"Failed to get progress summary: {str(e)}")


# Example usage
if __name__ == "__main__":
    tracker = initialize_progress_tracker()
    tracker = update_progress_tracker(tracker, 'pending', 'task_1')
    tracker = update_progress_tracker(tracker, 'completed', 'task_2')
    tracker = update_progress_tracker(tracker, 'failed', 'task_3')
    summary = get_progress_summary(tracker)
    print(summary)
