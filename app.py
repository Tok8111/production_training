import sqlite3
import calendar
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from datetime import datetime, timedelta

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
# カレンダー形式データ作成
# ---------------------------
def generate_calendar(year, month):
    # その月の日数・曜日情報を取得してカレンダー形式データを作成
    cal = calendar.Calendar(firstweekday=6)  # 日曜始まりに調整（必要に応じて）
    month_days = cal.monthdayscalendar(year, month)  # [[日〜土]の日にち(0=空白)]

    return month_days

# ---------------------------
# 利用者一覧データ作成
# ---------------------------
@app.route('/user_list')
def user_list():
    if 'username' not in session or session['role'] != 'staff':
        return redirect(url_for('index'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username FROM users WHERE role = 'user'")
    users = cursor.fetchall()
    conn.close()

    return render_template('user_list.html', users=users)

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
            session['user_id'] = user['user_id'] # ユーザIDをセッションに保存
            session['username'] = user['username']  # ユーザネームをセッションに保存
            session['role'] = user['role']  # ユーザロールをセッションに保存
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
    if 'username' not in session or 'role' not in session:
        return redirect(url_for('index'))

    role = session['role']
    username = session['username']

    calendar_data = None
    year = None
    month = None
    prev_year = prev_month = next_year = next_month = None
    users = []  # 追加：staff用の利用者一覧

    if role == 'user':
        # クエリパラメータから年月取得。無ければ今月
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        today = datetime.today()
        if not year:
            year = today.year
        if not month:
            month = today.month

        calendar_data = generate_calendar(year, month)

        first_day = datetime(year, month, 1)
        prev_month_date = first_day - timedelta(days=1)
        next_month_date = first_day + timedelta(days=31)
        next_month_date = datetime(next_month_date.year, next_month_date.month, 1)

        prev_year, prev_month = prev_month_date.year, prev_month_date.month
        next_year, next_month = next_month_date.year, next_month_date.month

    elif role == 'staff':
        # 利用者一覧を取得
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name FROM users WHERE role = 'user'")
        rows = cursor.fetchall()
        users = [{'id': row['user_id'], 'name': row['name']} for row in rows]
        conn.close()

    return render_template('main.html',
                           username=username,
                           role=role,
                           calendar=calendar_data,
                           year=year,
                           month=month,
                           prev_year=prev_year,
                           prev_month=prev_month,
                           next_year=next_year,
                           next_month=next_month,
                           users=users)  # 追加

# -----------------------
# G4. 日報入力画面のルート
# -----------------------
@app.route('/daily_report_input', methods=['GET', 'POST'])
def daily_report_input():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if request.method == 'POST':
        date = request.form['date']
        work_type = request.form['work_type']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        content = request.form['content']
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

    # ★ここを追加：GETパラメータから日付取得
    selected_date = request.args.get('date')
    if selected_date is None:
        selected_date = datetime.today().strftime('%Y-%m-%d')

    return render_template(
        'daily_report_input.html',
        username=username,
        date=selected_date  # ★テンプレートに渡す
    )

# -----------------------
# G5. 日報一覧画面のルート
# -----------------------
# @app.route('/report_list', methods=['GET', 'POST'])
# def report_list():
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     username = session['username']
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute('''
#         SELECT reports.*, users.username 
#         FROM reports
#         JOIN users ON reports.user_id = users.user_id
#         WHERE users.username = ?
#         ORDER BY reports.report_date DESC
#     ''', (username,))

#     # cursor.execute('SELECT * FROM reports WHERE username = ? ORDER BY date DESC', (username,))

#     reports = cursor.fetchall()
#     conn.close()
#     return render_template('report_list.html', reports=reports, username=username)


# -----------------------
# G5. 日報一覧画面のルート
# -----------------------
@app.route('/report_list')
def report_list():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = request.args.get('user_id')
    role = session.get('role')
    username = session['username']

    conn = get_db()
    cursor = conn.cursor()

    if role == 'staff' and user_id:
        # 職員が指定利用者の日報を閲覧
        cursor.execute('''
            SELECT reports.*, users.username 
            FROM reports
            JOIN users ON reports.user_id = users.user_id
            WHERE users.user_id = ?
            ORDER BY reports.report_date DESC
        ''', (user_id,))
    else:
        # 自分の日報を閲覧（利用者）
        cursor.execute('''
            SELECT reports.*, users.username 
            FROM reports
            JOIN users ON reports.user_id = users.user_id
            WHERE users.username = ?
            ORDER BY reports.report_date DESC
        ''', (username,))

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
# アプリ起動
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)