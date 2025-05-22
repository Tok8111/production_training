import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('your_database.db')  # DBファイル名に適宜変更
    cursor = conn.cursor()

    # 既存の users テーブルを削除（初期化のため）
    cursor.execute('DROP TABLE IF EXISTS users')

    # users テーブル再作成
    cursor.execute('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT
        )
    ''')

    now = datetime.now().isoformat()

    # 仮の利用者アカウント
    cursor.execute('''
        INSERT INTO users (username, password, name, role, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', ('test_user', 'pass123', 'テスト利用者', 'user', now))

    # 仮の職員アカウント
    cursor.execute('''
        INSERT INTO users (username, password, name, role, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', ('staff_user', 'pass123', 'テスト職員', 'staff', now))

    conn.commit()
    conn.close()
    print("usersテーブルを再作成しました")

if __name__ == '__main__':
    init_db()