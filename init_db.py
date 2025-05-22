import sqlite3

conn = sqlite3.connect('your_database.db')  # 実際のDBファイル名に置き換えてください
cursor = conn.cursor()

# usersテーブル作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# # テストユーザー追加
# cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('testuser', 'testpass'))

# conn.commit()
# conn.close()

# print("テストユーザーを追加しました。")

# reports テーブル作成（存在しない場合）
cursor.execute('''
CREATE TABLE IF NOT EXISTS reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    report_date DATE NOT NULL,
    condition TEXT NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    work_time INTEGER NOT NULL,
    work_detail TEXT NOT NULL,
    user_comment TEXT,
    staff_comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
''')

conn.commit()
conn.close()

print("テーブル 'reports' を作成しました。")