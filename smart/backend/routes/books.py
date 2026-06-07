from importlib.resources import path
import os

from flask import flash, session
from backend.services.sms_service import send_alert_sms
from flask import Blueprint, render_template, request, redirect, url_for
from backend.database.db import db
from sqlalchemy import text
import pickle
import numpy as np
from datetime import datetime, timedelta

books_bp = Blueprint('books', __name__, url_prefix='/books')

model_path = os.path.join('..', 'models', 'fine_model.pkl')

# @books_bp.route('/books')
# def view_books():
#     books = db.session.execute(text("SELECT * FROM books")).fetchall()
#     return render_template('books.html', books=books)

@books_bp.route('/books')
def view_books():
    category = request.args.get('category')   # category filter
    search = request.args.get('search')       # search input

    query = "SELECT id, title, author, category, quantity FROM books WHERE 1=1"
    params = {}

    # Category filter
    if category:
        query += " AND category = :category"
        params['category'] = category

    # Search filter (title + author)
    if search:
        query += " AND (title LIKE :search OR author LIKE :search)"
        params['search'] = f"%{search}%"

    books = db.session.execute(text(query), params).fetchall()

    return render_template('books.html', books=books)

@books_bp.route('/notify', methods=['POST'])
def notify_user():
    book_name = request.form.get('book_name')
    phone = request.form.get('phone')

    db.session.execute(
        text("""
        INSERT INTO notifications (book_name, phone)
        VALUES (:book, :phone)
        """),
        {'book': book_name, 'phone': phone}
    )
    db.session.commit()

    return "✅ You will be notified when book is available!"


@books_bp.route('/add-book', methods=['GET', 'POST'])
def add_book():

    # 🔐 Admin check
    if session.get('role') != 'admin':
        return "Access Denied ❌"

    title = request.form.get('title')
    author = request.form.get('author')
    category = request.form.get('category')

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.session.execute(
        text("""
        INSERT INTO books (title, author, category, created_at)
        VALUES (:title, :author, :category, :created_at)
        """),
        {
            'title': title,
            'author': author,
            'category': category,
            'created_at': created_at
        }
    )

    db.session.commit()

    return "✅ Book Added Successfully"


@books_bp.route('/issue-book', methods=['POST'])
def issue_book():
    # users_id = session.get('users_id')
    users_id = session.get('user_id')  # ensure this exists

    role = session.get('role') 

    book_id = request.form['book_id']

    book = db.session.execute(
        text("SELECT title FROM books WHERE id=:id"),
        {'id': book_id}
    ).fetchone()

    book_name = book.title 
    issue_datetime = datetime.now()
    due_datetime = issue_datetime + timedelta(days=7)

    db.session.execute(
        text("""
        INSERT INTO issued_books
        (users_id, book_name, issue_date, due_date)
        VALUES (:users_id, :book_name, :issue_date, :due_date)
        """),
        {
            'users_id': users_id,
            'book_name': book_name,
            'issue_date': issue_datetime,
            'due_date': due_datetime
        }
    )


    db.session.commit()
    
    db.session.commit()

    print("CALLING SMS NOW")

    user_phone = db.session.execute(
    text("SELECT phone FROM users WHERE id=:id"),
    {"id": session.get('user_id')}
    ).fetchone()

    if user_phone:
     phone = user_phone.phone
    message = "Book issued successfully"
    send_alert_sms(phone, message)

    flash("Book Issued Successfully ✅", "success")

    if session.get('role') == 'admin':
     return redirect(url_for('admin.dashboard'))
    else:
     return redirect(url_for('books.view_books'))
    

@books_bp.route('/return', methods=['POST'])
def return_book():

    if session.get('role') != 'admin':
        return "Access Denied ❌"

    issue_id = request.form.get('issue_id')

    if not issue_id:
        return "❌ Issue ID required!"

    issue_id = int(issue_id)

    # 🔍 Get issued book
    issue = db.session.execute(
        text("SELECT * FROM issued_books WHERE id=:id"),
        {'id': issue_id}
    ).fetchone()

    if not issue:
        return "❌ Invalid Issue ID!"

    # ❗ Safety check (already returned?)
    if issue.return_date:
        return "⚠️ Book already returned!"

    return_date = datetime.now()

    # ❗ Handle NULL due_date (important)
    if not issue.due_date:
        return "❌ Due date missing in DB!"

    due_date = issue.due_date

    # 📅 Calculate delay
    days_late = (return_date.date() - due_date.date()).days
    days_late = max(0, days_late)

    # 💰 Fine calculation

#     days_late = return_date - due_date

# if days_late > 0:
#     fine = ML model predicts fine
# else:
#     fine = 0

    fine = 0
    if days_late > 0:
        fine = int(fine_model.predict(np.array([[days_late]]))[0])

    # 🔥 Update issued_books
    result = db.session.execute(
        text("""
        UPDATE issued_books
        SET return_date=:r, fine=:f
        WHERE id=:id
        """),
        {
            'r': return_date,
            'f': fine,
            'id': issue_id
        }
    )

    print("Updated Rows:", result.rowcount)  # 🔥 DEBUG

    # ⚠️ Check if update failed
    if result.rowcount == 0:
        return "❌ Update failed! Check Issue ID"

    # 🔥 OPTIONAL: only if book_id exists in table
    if hasattr(issue, 'book_id') and issue.book_id:
        db.session.execute(
            text("UPDATE books SET available=1 WHERE id=:book_id"),
            {'book_id': issue.book_id}
        )

    db.session.commit()

    return (
        f"✅ Book Returned Successfully<br>"
        f"📅 Days Late: {days_late}<br>"
        f"💰 Fine: ₹{fine}"
    )

@books_bp.route('/send-alert', methods=['POST'])
def send_alert_route():
    phone = request.form.get('phone')      # ✔ key name
    message = request.form.get('message')

    # if not phone or not message:
    #     return "Phone or message missing", 400

    send_alert_sms(phone, message)
    return "Alert SMS sent successfully"

