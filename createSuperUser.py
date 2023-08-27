import mysql.connector

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
my_ip = s.getsockname()[0]
s.close()


mydb = mysql.connector.connect(
    host=my_ip,
    user="root",
    passwd="root",
    database="joke-app-db"
)


mycursor = mydb.cursor()
sql = "INSERT INTO users_table (user, pswd, role, token) VALUES (%s, %s,%s,%s)"
val = ("admin", "dk-automation", "admin", "IS_NULL")
mycursor.execute(sql, val)
mydb.commit()
print(" admin user record inserted.")


mycursor = mydb.cursor()
sql = "INSERT INTO users_table (user, pswd, role, token) VALUES (%s, %s,%s,%s)"
val = ("product", "infraprod", "supernova", "IS_NULL")
mycursor.execute(sql, val)
mydb.commit()

print(" supernova user record inserted.")
