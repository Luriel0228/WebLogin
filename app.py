from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# SQLite3 데이터베이스 생성 및 연결
conn = sqlite3.connect('users.db', check_same_thread=False)
conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    cursor = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return "잘못된 사용자 이름 또는 비밀번호"

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')

    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()

    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"안녕하세요, {session['username']}님! 대시보드에 오신 것을 환영합니다."
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)