import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('your_database.db')  # 必要に応じて変更
    cursor = conn.cursor()

    # 初期化のためのテーブル削除
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

    # 利用者 5名
    users_data = [
        ('user01', 'pass1', '利用者 一郎', 'user', now),
        ('user02', 'pass2', '利用者 二郎', 'user', now),
        ('user03', 'pass3', '利用者 三郎', 'user', now),
        ('user04', 'pass4', '利用者 四郎', 'user', now),
        ('user05', 'pass5', '利用者 五郎', 'user', now),

        # 職員 2名
        ('staff01', 'pass01', '佐藤 太郎', 'staff', now),
        ('staff02', 'pass02', '鈴木 次郎', 'staff', now)
    ]

    cursor.executemany('''
        INSERT INTO users (username, password, name, role, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', users_data)

    conn.commit()
    conn.close()
    print("データベース初期化完了：users・reports・report_tasks テーブル作成＆初期データ投入済")

if __name__ == '__main__':
    init_db()