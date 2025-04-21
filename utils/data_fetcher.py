# utils/data_fetcher.py

import mysql.connector
from mysql.connector import Error
import logging

def fetch_migration_data(database_config):
    """
    Fetches migration data from the source database to be used by the progress and status trackers.

    Args:
        database_config (dict): Configuration dictionary for the database connection.

    Returns:
        list: A list of dictionaries containing migration data.

    Raises:
        Exception: If there is an error fetching data from the database.
    """
    
    try:
        # Establishing the database connection
        connection = mysql.connector.connect(
            host=database_config["host"],
            user=database_config["user"],
            password=database_config["password"],
            database=database_config["database"]
        )
        
        if connection.is_connected():
            logging.info("Connected to the database successfully")
            cursor = connection.cursor(dictionary=True)

            # Executing the query to fetch migration data
            query = "SELECT * FROM migration_data"
            cursor.execute(query)
            records = cursor.fetchall()
            logging.info(f"Fetched {len(records)} records from the database")

            return records

    except Error as e:
        logging.error(f"Error fetching data from the database: {str(e)}")
        raise Exception(f"Error fetching data from the database: {str(e)}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logging.info("Database connection closed")

