from flask import Flask, render_template, request, redirect
import sqlite3
import string
import random

app = Flask(__name__)
conn = sqlite3.connect('urls.db',check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        short_code TEXT NOT NULL
    )
''')
conn.commit()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        short_code = generate_short_code()
        c.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
        conn.commit()
        return redirect('/success/' + short_code)
    return render_template('index.html')

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/success/<short_code>')
def success(short_code):
    return render_template('success.html', short_code=short_code)

@app.route('/<short_code>')
def redirect_to_url(short_code):
    c.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    result = c.fetchone()
    if result:
        original_url = result[0]
        return redirect(original_url)
    return 'Invalid URL'

if __name__ == '__main__':
    app.run(debug=True)
