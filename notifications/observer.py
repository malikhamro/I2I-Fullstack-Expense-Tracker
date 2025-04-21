import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .change_notifier import send_notification

class ConfigChangeHandler(FileSystemEventHandler):
    """
    Event handler for detecting changes in configuration files.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def on_modified(self, event):
        if event.src_path == self.file_path:
            # Trigger send_notification with sample details
            send_notification(f"Configuration file {self.file_path} has been modified.")

def watch_config_changes(config_path):
    """
    Monitors the configuration files or settings for any changes.
    Upon detecting a change, it triggers the `send_notification` function.
    
    :param config_path: Path to the configuration file that needs to be monitored.
    """
    if not os.path.isfile(config_path):
        raise ValueError(f"The path {config_path} is not a valid file.")
    
    event_handler = ConfigChangeHandler(config_path)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(config_path), recursive=False)
    
    print(f"Start watching {config_path} for changes...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping observer...")
        observer.stop()
    observer.join()
