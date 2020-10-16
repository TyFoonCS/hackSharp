import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute('DELETE from users')

conn.commit()
