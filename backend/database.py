import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="erito_learning"
)

print("Database connection successful!")

connection.close()