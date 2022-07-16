#Importing necessary packages
import mysql.connector as mariadb

#adding a mariadb object, and connecting to the database
mydb = mariadb.connect(host="localhost", user="pythonscript_user",passwd = "pythonpassword")
#Adding a database cursor object
db_cursor = mydb.cursor()

#executing SQL queries with the cursor

db_cursor.execute("show databases")

for i in db_cursor:
    print(i)