from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ensure database exists
def init_db():
    conn = sqlite3.connect('news.db')
    conn.execute("""CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT
    )""")
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('news.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM news ORDER BY id DESC LIMIT 1")
    news = cur.fetchone()
    conn.close()
    return render_template('frontend.html', news=news)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'ntpc@123':
            session['admin'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('add_news'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('Logged out!', 'info')
    return redirect(url_for('admin_login'))

@app.route('/add-news', methods=['GET', 'POST'])
def add_news():
    if 'admin' not in session:
        flash('Login required', 'warning')
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        conn = sqlite3.connect('news.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO news (title, message, start_date, end_date) VALUES (?, ?, ?, ?)",
                    (title, message, start_date, end_date))
        conn.commit()
        conn.close()
        flash('News posted successfully!', 'success')
        return redirect(url_for('add_news'))
    return render_template('add_news.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
