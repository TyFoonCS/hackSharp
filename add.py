import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute('insert into users values("grob", "grobik", "0000", "МБОУ ИТ-лицей №24", 1, "Не указаны", 0)')
conn.commit()
