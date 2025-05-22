import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'your_database.db'  # SQLiteのDBファイル

# ---------------------------
# DB接続管理
# ---------------------------
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('your_database.db')
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# ---------------------------
# G1.トップページ（ログイン画面）
# ---------------------------
@app.route('/')
def index():
    return render_template('login.html')

# ---------------------------
# ログイン処理
# ---------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            return redirect(url_for('main'))
        else:
            return redirect(url_for('login_failure'))
    
    # GETリクエスト時のフォーム表示
    return render_template('login.html')

# ---------------------------
# G2.ログイン失敗処理（ログイン失敗画面へ遷移）
# ---------------------------
@app.route('/login_failure')
def login_failure():
    return render_template('login_failure.html')

# ---------------------------
# G3.メイン画面
# ---------------------------
@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'username' in session:
        return render_template('main.html', username=session['username'])
    else:
        return redirect(url_for('index'))

# -----------------------
# G4. 日報入力画面のルート
# -----------------------
@app.route('/daily_report_input', methods=['GET', 'POST'])
def daily_report_input():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        date = request.form['date']
        work_type = request.form['work_type']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        content = request.form['content']
        username = session['username']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reports (username, date, work_type, start_time, end_time, content, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, date, work_type, start_time, end_time, content, created_at))
        conn.commit()
        conn.close()
        flash('日報を登録しました。')
        return redirect(url_for('report_list'))

    return render_template('daily_report_input.html', username=session['username'])

# -----------------------
# G5. 日報一覧画面のルート
# -----------------------
@app.route('/report_list', methods=['GET', 'POST'])
def report_list():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT reports.*, users.username 
        FROM reports
        JOIN users ON reports.user_id = users.user_id
        WHERE users.username = ?
        ORDER BY reports.report_date DESC
    ''', (username,))

    # cursor.execute('SELECT * FROM reports WHERE username = ? ORDER BY date DESC', (username,))

    reports = cursor.fetchall()
    conn.close()
    return render_template('report_list.html', reports=reports, username=username)

# ---------------------------
# G6.ログアウト処理（ログアウト画面へ遷移）
# ---------------------------
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('logout.html')

# ---------------------------
# 以下、仮ルート（今後実装予定）
# ---------------------------

# 【仮】カレンダー（未実装）
@app.route('/calender', methods=['GET', 'POST'])
def calender():
    return render_template('calender.html')

# 【仮】利用者一覧（未実装）
@app.route('/user_list', methods=['GET', 'POST'])
def user_list():
    return render_template('user_list.html')

# ---------------------------
# アプリ起動
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)