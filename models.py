
# This file handles all our database connections and SQL queries.
# Instead of writing SQL inside our main web routes, we put them here 
# to keep the project clean and organized.
from datetime import date, timedelta

from db import get_db

# Setting default borrow time to two weeks
LOAN_PERIOD_DAYS = 14


# --- User Authentication DB Queries ---
def create_user(username, password_hash, role="librarian"):
    db = get_db()
    cur = db.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role),
    )
    db.commit()
    return cur.lastrowid


def get_user_by_username(username):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()


def get_user_by_id(user_id):
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


# --- Book Catalog DB Queries ---
def add_book(title, author, isbn, quantity):
    db = get_db()
    cur = db.execute(
        "INSERT INTO books (title, author, isbn, quantity, available) "
        "VALUES (?, ?, ?, ?, ?)",
        (title, author, isbn, quantity, quantity),
    )
    db.commit()
    return cur.lastrowid


def update_book(book_id, title, author, isbn, quantity):
    db = get_db()
    book = get_book(book_id)
    if book is None:
        return False
        
    # Figure out the difference if quantity is changed
    delta = quantity - book["quantity"]
    new_available = max(0, book["available"] + delta)
    db.execute(
        "UPDATE books SET title = ?, author = ?, isbn = ?, quantity = ?, "
        "available = ? WHERE id = ?",
        (title, author, isbn, quantity, new_available, book_id),
    )
    db.commit()
    return True


def remove_book(book_id):
    db = get_db()
    cur = db.execute("DELETE FROM books WHERE id = ?", (book_id,))
    db.commit()
    return cur.rowcount > 0


def get_book(book_id):
    db = get_db()
    return db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()


def search_books(query=""):
    db = get_db()
    like = f"%{query}%"
    return db.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? "
        "ORDER BY title",
        (like, like, like),
    ).fetchall()


def list_books():
    db = get_db()
    return db.execute("SELECT * FROM books ORDER BY title").fetchall()


# --- Book Issuing and Return Queries ---
def issue_book(book_id, borrower, issued_by):
    db = get_db()
    book = get_book(book_id)
    if book is None or book["available"] < 1:
        return None
        
    # Reduce available count by 1 since it's going out
    db.execute(
        "UPDATE books SET available = available - 1 WHERE id = ?", (book_id,)
    )
    # Calculate the due date automatically
    due = date.today() + timedelta(days=LOAN_PERIOD_DAYS)
    cur = db.execute(
        "INSERT INTO loans (book_id, borrower, issued_by, due_date, status) "
        "VALUES (?, ?, ?, ?, 'issued')",
        (book_id, borrower, issued_by, due.isoformat()),
    )
    db.commit()
    return cur.lastrowid


def return_book(loan_id):
    db = get_db()
    loan = db.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
    if loan is None or loan["status"] == "returned":
        return False
        
    # Mark as returned and stamp the time
    db.execute(
        "UPDATE loans SET status = 'returned', return_date = CURRENT_TIMESTAMP "
        "WHERE id = ?",
        (loan_id,),
    )
    # Put the book copy back into available count
    db.execute(
        "UPDATE books SET available = available + 1 WHERE id = ?",
        (loan["book_id"],),
    )
    db.commit()
    return True


def list_active_loans():
    db = get_db()
    # Join tables to get both book titles and loan info together
    return db.execute(
        "SELECT loans.id, loans.borrower, loans.issue_date, loans.due_date, "
        "books.title, books.author "
        "FROM loans JOIN books ON loans.book_id = books.id "
        "WHERE loans.status = 'issued' "
        "ORDER BY loans.due_date"
    ).fetchall()


def list_overdue_loans():
    db = get_db()
    today = date.today().isoformat()
    # Filter where status is issued and today is past due date
    return db.execute(
        "SELECT loans.id, loans.borrower, loans.due_date, books.title "
        "FROM loans JOIN books ON loans.book_id = books.id "
        "WHERE loans.status = 'issued' AND loans.due_date < ? "
        "ORDER BY loans.due_date",
        (today,),
    ).fetchall()


# --- Dashboard Counter Queries ---
def get_summary_stats():
    db = get_db()
    total_books = db.execute("SELECT COALESCE(SUM(quantity), 0) AS n FROM books").fetchone()["n"]
    available = db.execute("SELECT COALESCE(SUM(available), 0) AS n FROM books").fetchone()["n"]
    active_loans = db.execute(
        "SELECT COUNT(*) AS n FROM loans WHERE status = 'issued'"
    ).fetchone()["n"]
    overdue = len(list_overdue_loans())
    return {
        "total_books": total_books,
        "available_books": available,
        "active_loans": active_loans,
        "overdue_loans": overdue,
    }