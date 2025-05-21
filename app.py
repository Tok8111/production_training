from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb.cursors
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your secret key'

# MySQLの設定
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'yourusername'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'yourdatabase'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['user_id']
            return redirect(url_for('main'))
        else:
            error = 'ユーザー名またはパスワードが正しくありません。'
    return render_template('login.html', error=error)

@app.route('/main')
def main():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT username FROM users WHERE user_id = %s', (user_id,))
    user = cursor.fetchone()
    username = user['username'] if user else '利用者'

    return render_template('main.html', username=username)

@app.route('/report_input')
def report_input():
    return "日報入力画面（未実装）"

@app.route('/report_list')
def report_list():
    return "日報一覧画面（未実装）"

@app.route('/user_list')
def user_list():
    return "利用者一覧画面（未実装）"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)