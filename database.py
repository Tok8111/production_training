import sqlite3

conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()
cursor.execute('''
SELECT * FROM reports
''')
for row in cursor.fetchall():
    print(row)
conn.close()