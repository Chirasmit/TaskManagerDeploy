import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="taskman"
)

cursor = db.cursor()