from flask import Blueprint, request, redirect, url_for
from backend.database.db import db
from sqlalchemy import text

students_bp = Blueprint('students', __name__)

@students_bp.route('/add-student', methods=['POST'])
def add_student():
    name = request.form['name']
    phone = request.form['phone']

    db.session.execute(
        text("INSERT INTO students(name, phone) VALUES(:name, :phone)"),
        {'name': name, 'phone': phone}
    )
    db.session.commit() 

    return redirect(url_for('auth.dashboard'))

@students_bp.route('/book_issue', methods=['POST'])
def book_issue():
    users_id = request.form.get('users_id')
    book_name = request.form.get('book_name')

    db.session.execute(
        text("INSERT INTO issued_books(users_id, book_name) VALUES(:users_id, :book_name)"),
        {'users_id': users_id, 'book_name': book_name}
    )
    db.session.commit()

    # save issue record in database
    return "Book Issued"


@students_bp.route('/book_return', methods=['POST'])
def book_return():
    users_id = request.form.get('users_id')
    book_name = request.form.get('book_name')

    db.session.execute(
        text("UPDATE issued_books SET return_date = CURRENT_DATE WHERE users_id = :users_id AND book_name = :book_name AND return_date IS NULL"),
        {'users_id': users_id, 'book_name': book_name}
    )
    db.session.commit()
    # return book using users_id
    return "Book Returned"
