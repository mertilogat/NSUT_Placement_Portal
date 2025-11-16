"""
Database connection module for NSUT Placement Portal
Provides MySQL connection and query execution utilities
Uses mysql-connector-python (no ORM)
"""

import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    """
    Create and return a MySQL database connection
    
    Returns:
        connection: MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        
        if connection.is_connected():
            return connection
        else:
            print("Failed to connect to database")
            return None
            
    except Error as e:
        print(f"Database connection error: {e}")
        return None


def execute_query(query, params=None, fetch=False, fetch_one=False):
    """
    Execute a SQL query with prepared statements (prevents SQL injection)
    
    Args:
        query (str): SQL query with %s placeholders for parameters
        params (tuple): Parameters to substitute in query
        fetch (bool): If True, return all results (SELECT queries)
        fetch_one (bool): If True, return only first result
        
    Returns:
        For SELECT: list of dictionaries (if fetch=True) or single dict (if fetch_one=True)
        For INSERT/UPDATE/DELETE: number of affected rows or lastrowid for INSERT
        None if error occurs
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)  # Return results as dictionaries
        
        # Execute query with parameters (prepared statement)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Handle SELECT queries (fetch results)
        if fetch or fetch_one:
            if fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        
        # Handle INSERT/UPDATE/DELETE queries (commit changes)
        else:
            connection.commit()
            affected_rows = cursor.rowcount
            last_id = cursor.lastrowid
            cursor.close()
            connection.close()
            
            # Return last inserted ID for INSERT queries, otherwise affected rows
            return last_id if last_id > 0 else affected_rows
            
    except Error as e:
        print(f"Query execution error: {e}")
        if connection:
            connection.close()
        return None


def test_connection():
    """
    Test database connection
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    connection = get_db_connection()
    if connection:
        print("✓ Database connection successful")
        connection.close()
        return True
    else:
        print("✗ Database connection failed")
        return False


# Helper function for common queries
def get_by_id(table, id_value, id_column='id'):
    """
    Fetch a single record by ID
    
    Args:
        table (str): Table name
        id_value: Value to search
        id_column (str): Column name (default: 'id')
        
    Returns:
        dict: Single record or None
    """
    query = f"SELECT * FROM {table} WHERE {id_column} = %s"
    return execute_query(query, (id_value,), fetch_one=True)


def get_all(table, where_clause=None, params=None, order_by=None):
    """
    Fetch all records from a table with optional filtering
    
    Args:
        table (str): Table name
        where_clause (str): Optional WHERE clause (without WHERE keyword)
        params (tuple): Parameters for WHERE clause
        order_by (str): Optional ORDER BY clause
        
    Returns:
        list: List of records
    """
    query = f"SELECT * FROM {table}"
    
    if where_clause:
        query += f" WHERE {where_clause}"
    
    if order_by:
        query += f" ORDER BY {order_by}"
    
    return execute_query(query, params, fetch=True)
