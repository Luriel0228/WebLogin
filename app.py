from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn = sqlite3.connect('users.db', check_same_thread=False)
conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password_salt TEXT, password_hash TEXT)')

def hash_password(password, salt=None, iterations=100000):
    if salt is None:
        salt = os.urandom(32)

    hash_result = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations,
        dklen=128
    )

    return salt, hash_result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    cursor = conn.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if user:
        stored_salt = user[1]
        stored_hashed_password = user[2]

        _, hashed_password = hash_password(password, salt=stored_salt)

        if hashed_password == stored_hashed_password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "잘못된 사용자 이름 또는 비밀번호"
    else:
        return "잘못된 사용자 이름 또는 비밀번호"

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')

    salt, hashed_password = hash_password(password)
    conn.execute('INSERT INTO users (username, password_salt, password_hash) VALUES (?, ?, ?)', (username, salt, hashed_password))
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