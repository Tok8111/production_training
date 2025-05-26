import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('your_database.db')  # 必要に応じてファイル名変更
    cursor = conn.cursor()

    # 既存テーブルの削除（初期化目的）
    cursor.execute('DROP TABLE IF EXISTS report_tasks')
    cursor.execute('DROP TABLE IF EXISTS reports')
    cursor.execute('DROP TABLE IF EXISTS users')

    # users テーブル作成
    cursor.execute('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # reports テーブル作成
    cursor.execute('''
        CREATE TABLE reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            report_date DATE NOT NULL,
            condition TEXT NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            work_time INTEGER NOT NULL,
            work_detail TEXT NOT NULL,
            user_comment TEXT,
            staff_comment TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')

    # report_tasks テーブル作成
    cursor.execute('''
        CREATE TABLE report_tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            task_order INTEGER NOT NULL,
            task_name TEXT NOT NULL,
            task_duration INTEGER NOT NULL,
            task_note TEXT,
            FOREIGN KEY (report_id) REFERENCES reports(report_id)
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
    print("users・reports・report_tasks テーブルを作成・初期化しました")

if __name__ == '__main__':
    init_db()