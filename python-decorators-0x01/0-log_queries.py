import sqlite3
import functools

# Step 1: Define the decorator
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Step 2: Extract the SQL query from args or kwargs
        query = kwargs.get("query") if "query" in kwargs else args[0] if args else None
        
        # Step 3: Log the SQL query
        print(f"[LOG] Executing SQL Query: {query}")
        
        # Step 4: Call the original function
        return func(*args, **kwargs)
    
    return wrapper

# Step 5: Use the decorator
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Step 6: Call the function with logging
users = fetch_all_users(query="SELECT * FROM users")
