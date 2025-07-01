# src/database.py

import sqlite3
from sqlite3 import Error

DATABASE = 'path/to/database.db'

def create_connection():
    """ Create a database connection to the SQLite database
        specified by DATABASE
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)
    return conn

def update_claim_status_in_db(claim_id, new_status):
    """
    Update the status of a specific claim in the database.
    :param claim_id: ID of the claim to update
    :param new_status: New status to be set for the claim
    :return: True if update is successful, False otherwise
    """
    sql = '''UPDATE claims
             SET status = ?
             WHERE id = ?'''
    conn = create_connection()
    if conn is None:
        return False
    try:
        cur = conn.cursor()
        cur.execute(sql, (new_status, claim_id))
        conn.commit()
        return cur.rowcount == 1
    except Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_claim_by_id(claim_id):
    """
    Retrieve a claim's details using its ID.
    :param claim_id: ID of the claim to fetch
    :return: Dictionary containing claim details if found, None otherwise
    """
    sql = '''SELECT * FROM claims WHERE id = ?'''
    conn = create_connection()
    if conn is None:
        return None
    try:
        cur = conn.cursor()
        cur.execute(sql, (claim_id,))
        row = cur.fetchone()
        return dict(zip([column[0] for column in cur.description], row)) if row else None
    except Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()
