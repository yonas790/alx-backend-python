import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv() 

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dbname = os.getenv("DB_NAME")
host = os.getenv("DB_HOST")

def get_db_connection():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=dbname
    )

def stream_users_in_batches(batch_size):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    offset = 0

    while True:
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (batch_size, offset))
        rows = cursor.fetchall()

        if not rows:
            break

        yield rows
        offset += batch_size

    cursor.close()
    conn.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
