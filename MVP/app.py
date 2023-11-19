# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from User.Client.base import ClientBase
from database.db import DB
from config import MONGO_DB_URI

app = Flask(__name__)
app.secret_key = 'your_secret_key'
db_instance = DB()
client_base = ClientBase(db_instance)

@app.route('/')
def landing_page():
    return render_template('index.html')

@app.route('/select_account_type', methods=['GET', 'POST'])
def select_account_type():
    if request.method == 'POST':
        account_type = request.form.get('account_type')
        if account_type == 'client':
            return redirect(url_for('client'))
    return render_template('types.html')

@app.route('/client', methods=['GET', 'POST'])
def client():
    message = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        action = request.form.get('action')

        data = {
            'username': username,
            'password': password,
            'email': email,
            'action': action,
            'user_type': 'client'
        }

        result = client_base.handle_login_or_signup(data)

        if 'user_id' in result or 'user_created' in result:
            flash('Login or signup successful!', 'success')
            return redirect('/dashboard')
        else:
            message = result.get('error', 'Invalid credentials')

    return render_template('client.html', message=message)

@app.route('/company')
def company():
    flash('Welcome to the Company Page!', 'info')
    return render_template('company.html')

@app.route('/worker')
def worker():
    flash('Welcome to the Worker Page!', 'info')
    return render_template('worker.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
