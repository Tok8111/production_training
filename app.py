from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション管理に必要

# 仮のユーザーデータ（後でDB連携予定）
dummy_users = {
    "user01": "pass1234",
    "user02": "abcd5678"
}

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in dummy_users and dummy_users[username] == password:
            session['username'] = username
            return redirect(url_for('main'))
        else:
            error = 'ユーザーIDまたはパスワードが正しくありません。'

    return render_template('login.html', error=error)

@app.route('/main')
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    return f"{session['username']} さん、ようこそ！メイン画面へ"

if __name__ == '__main__':
    app.run(debug=True)
    