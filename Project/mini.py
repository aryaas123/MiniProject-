from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import pickle
import numpy as np
import os
import webbrowser

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ---------- MODEL LOADING ----------
model_path = os.path.join(os.getcwd(), 'gold_price_model.pkl')
model = pickle.load(open(model_path, 'rb'))

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# ---------- ROUTES ----------
@app.route('/')
def welcome():
    """Show the welcome page with gold image."""
    return render_template('welcome.html')

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('predict'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (uname, password))
            conn.commit()
            conn.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (uname, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = uname
            flash('Login successful!', 'success')
            return redirect(url_for('predict'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    prediction_text = None
    if request.method == 'POST':
        try:
            f1 = float(request.form['feature1'])
            f2 = float(request.form['feature2'])
            f3 = float(request.form['feature3'])
            f4 = float(request.form['feature4'])
            features = np.array([[f1, f2, f3, f4]])
            prediction = model.predict(features)[0]
            prediction_text = f'Predicted Gold Price: ₹{prediction:.2f}'
        except Exception as e:
            prediction_text = f"Error: {str(e)}"

    return render_template('home.html', username=session['username'], prediction_text=prediction_text)

@app.route('/goldshops')
def goldshops():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Static gold shops around Chengannur
    shops = [
        {"name": "Edimannical", "lat": 9.3285, "lon": 76.5732},
        {"name": "Sky Jwellery", "lat": 9.3240, "lon": 76.5700},
        {"name": "Pulimuttil Jeweelers", "lat": 9.3302, "lon": 76.5695},
        {"name": "New Rajadhani Gold and Diamonds", "lat": 9.3270, "lon": 76.5740},
        {"name": "Vismaya Gold", "lat": 9.3255, "lon": 76.5720}
    ]
    return render_template('goldshop.html', username=session['username'], shops=shops)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))

# ---------- AUTO OPEN BROWSER ----------
if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
