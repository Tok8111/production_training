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
            error = 'ユーザー名またはパスワードが間違っています。'
            return render_template('login.html', error=error)
    
    # GETリクエスト時のフォーム表示
    return render_template('login.html')

# ---------------------------
# メイン画面
# ---------------------------
@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'username' in session:
        return render_template('main.html', username=session['username'])
    else:
        return redirect(url_for('index'))

# ---------------------------
# ログアウト処理
# ---------------------------
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

# ---------------------------
# 以下、仮ルート（今後実装予定）
# ---------------------------

# 【仮】日報カレンダー（未実装）
@app.route('/daily_report_input', methods=['GET', 'POST'])
def daily_report_input():
    return render_template('daily_report_input.html')

# 【仮】日報一覧（未実装）
@app.route('/report_list', methods=['GET', 'POST'])
def report_list():
    return render_template('report_list.html')

# 【仮】利用者一覧（未実装）
@app.route('/user_list', methods=['GET', 'POST'])
def user_list():
    return render_template('user_list.html')

# ---------------------------
# アプリ起動
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)