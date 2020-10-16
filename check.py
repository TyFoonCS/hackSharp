import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute('select * from users')
print(cursor.fetchall())

