"""
Configuration settings for the backup and recovery processes.
"""

import os
import json

class Config:
    @staticmethod
    def get_backup_settings(config_file_path='config/backup_settings.json'):
        """
        Retrieve configuration settings related to backup such as backup frequency, storage location, etc.
        
        :param config_file_path: Path to the configuration file
        :return: A dictionary containing backup settings
        """
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"Configuration file for backup settings not found: {config_file_path}")
        
        try:
            with open(config_file_path, 'r') as file:
                settings = json.load(file)
                # Validate required settings
                if 'frequency' not in settings or 'storage_location' not in settings:
                    raise ValueError("Incomplete backup settings: 'frequency' and 'storage_location' are required.")
                
                return settings
        except json.JSONDecodeError:
            raise ValueError("Error decoding the backup settings configuration file.")
    
    @staticmethod
    def get_recovery_settings(config_file_path='config/recovery_settings.json'):
        """
        Retrieve configuration settings related to recovery processes.
        
        :param config_file_path: Path to the configuration file
        :return: A dictionary containing recovery settings
        """
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"Configuration file for recovery settings not found: {config_file_path}")
        
        try:
            with open(config_file_path, 'r') as file:
                settings = json.load(file)
                # Validate required settings
                if 'recovery_point' not in settings:
                    raise ValueError("Incomplete recovery settings: 'recovery_point' is required.")
                
                return settings
        except json.JSONDecodeError:
            raise ValueError("Error decoding the recovery settings configuration file.")
