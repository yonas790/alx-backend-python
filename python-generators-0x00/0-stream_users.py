import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv() 

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dbname = os.getenv("DB_NAME")
host = os.getenv("DB_HOST")

def stream_users():
    connection = mysql.connector.connect(
        host=host,
        user=user,        
        password=password,  
        database=dbname
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()


if __name__ == "__main__":
    for user in stream_users():
        print(user)
