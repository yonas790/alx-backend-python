import os
from dotenv import load_dotenv
import mysql.connector
import csv

load_dotenv() 

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dbname = os.getenv("DB_NAME")
host = os.getenv("DB_HOST")

def connect_db():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password, 
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=dbname
    )

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        );
    """)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, file_path):
    cursor = connection.cursor()
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (row["user_id"], row["name"], row["email"], row["age"]))
    connection.commit()
    cursor.close()
