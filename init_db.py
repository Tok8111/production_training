import sqlite3

conn = sqlite3.connect('your_database.db')  # 実際のDBファイル名に置き換えてください
cursor = conn.cursor()

# usersテーブル作成（なければ）
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# テストユーザー追加
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('testuser', 'testpass'))

conn.commit()
conn.close()

print("テストユーザーを追加しました。")