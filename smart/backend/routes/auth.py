from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database.db import db
from sqlalchemy import text
from flask import session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/logout')
def logout():
    return render_template('logout.html')


@auth_bp.route('/notification')
def notification():
    return render_template('notification.html')


@auth_bp.route('/')
def index():
    return render_template('index.html')


@auth_bp.route('/home')
def home():
    return render_template('home.html')




@auth_bp.route('/dashboard')
def dashboard():
    total_students = db.session.execute(text("SELECT COUNT(*) FROM students")).scalar()
    total_books = db.session.execute(text("SELECT COUNT(*) FROM books")).scalar()
    late_returns = db.session.execute(text("SELECT COUNT(*) FROM issued_books WHERE return_date IS NULL")).scalar()
    total_fine = db.session.execute(text("SELECT IFNULL(SUM(fine),0) FROM issued_books")).scalar()

    return render_template('dashboard.html', 
        total_students=total_students, 
        total_books=total_books,
        late_returns=late_returns,
        total_fine=total_fine
        )



@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.execute(text("SELECT * FROM users WHERE username=:username"), {'username': username}).fetchone()
        if user and check_password_hash(user.password, password):
            # ✅ Session set
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role

            print("Login Role:", user.role)

            # 🔥 ROLE BASED REDIRECT
            if user.role == 'admin':
             return redirect(url_for('auth.dashboard'))
            else:
             return redirect(url_for('auth.home'))
        return "Invalid credentials"
    return render_template('login.html')



@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = generate_password_hash(request.form['password'])
        db.session.execute(text("INSERT INTO users(username,email,password,phone) VALUES(:username,:email,:password,:phone)"),
                           {'username': username, 'email': email, 'password': password, 'phone': phone})
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html') 

