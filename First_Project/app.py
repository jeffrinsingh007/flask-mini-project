from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'

# SQL Server Config
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mssql+pyodbc://localhost\\SQLEXPRESS/testconnection"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class Try(db.Model):
    __tablename__ = 'try'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        hashed_password = generate_password_hash(data['password'])

        if Try.query.filter_by(email=data['email']).first():
            flash("Email already exists!", "danger")
            return redirect(url_for('signup'))

        new_user = Try(
            name=data['name'],
            gender=data['gender'],
            age=int(data['age']),
            address=data['address'],
            email=data['email'],
            phone=data['phone'],
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful. Please login.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Try.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = Try.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
