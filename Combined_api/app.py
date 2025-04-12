from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this!

DB_CONFIG = {
    'dbname': 'EV',
    'user': 'postgres',
    'password': '@Ankur7753',
    'host': 'localhost',
    'port': '5432'
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        is_admin = 'is_admin' in request.form  # Checkbox for admin registration

        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, email, password_hash, is_admin) VALUES (%s, %s, %s, %s)",
                        (username, email, hashed_password, is_admin))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
        except Exception as e:
            flash('Error during registration: ' + str(e), 'danger')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT username, password_hash, is_admin FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user'] = user[0]
            session['is_admin'] = user[2]
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard') if user[2] else url_for('user_dashboard'))
        flash('Invalid credentials.', 'danger')

    return render_template('login.html')

@app.route('/user_dashboard')
def user_dashboard():
    if 'user' not in session or session.get('is_admin'):
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    return render_template('user_dashboard.html', username=session['user'])

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' not in session or not session.get('is_admin'):
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    
    return render_template('admin_dashboard.html', username=session['user'])

# Routes for the three map pages
@app.route('/existing')
def existing_page():
    return render_template('Existing.html')

@app.route('/potential')
def potential_page():
    return render_template('Potential.html')

@app.route('/optimal')
def optimal_page():
    return render_template('Finaloptimal.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('is_admin', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
