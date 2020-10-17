import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute('insert into users values("bob", "bobik", "0000", "24", 0, "Чkil", 50)')
conn.commit()
