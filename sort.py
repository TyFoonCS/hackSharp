import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute('select fio, nick from users where school="МБОУ ИТ-лицей №24"')
print(cursor.fetchall())