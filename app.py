import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g

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
# トップページ（ログイン画面）
# ---------------------------
@app.route('/')
def index():
    return render_template('login.html')

# ---------------------------
# ログイン処理
# ---------------------------
@app.route('/login', methods=['POST'])
def login():
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
        error = 'ユーザー名またはパスワードが間違っています。'
        return render_template('login.html', error=error)

# ---------------------------
# メイン画面
# ---------------------------
@app.route('/main')
def main():
    if 'username' in session:
        return render_template('main.html', username=session['username'])
    else:
        return redirect(url_for('index'))

# ---------------------------
# ログアウト処理
# ---------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ---------------------------
# 以下、仮ルート（今後実装予定）
# ---------------------------

@app.route('/daily_report_input')
def daily_report_input():
    return "【仮】日報入力画面（未実装）"

@app.route('/report_history')
def report_history():
    return "【仮】過去の日報一覧（未実装）"

@app.route('/report_detail/<int:report_id>')
def report_detail(report_id):
    return f"【仮】日報詳細表示（ID: {report_id}）（未実装）"

@app.route('/export_csv')
def export_csv():
    return "【仮】CSV出力（未実装）"

@app.route('/user_settings')
def user_settings():
    return "【仮】ユーザー設定画面（未実装）"

# ---------------------------
# アプリ起動
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)