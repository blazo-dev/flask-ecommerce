import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="200875",
        database="flask_ecommerce_db"
    )
    print("Connection to MySQL was successful!")
    connection.close()
except Exception as e:
    print(f"Error: {e}")
