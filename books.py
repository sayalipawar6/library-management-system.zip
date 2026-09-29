"""Book management module: add, edit, remove, search / view books (CRUD)."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

import models
from utils import ValidationError, login_required, require_non_empty, require_positive_int

bp = Blueprint("books", __name__, url_prefix="/books")


@bp.route("/")
@login_required
def list_books():
    query = request.args.get("q", "").strip()
    books = models.search_books(query) if query else models.list_books()
    return render_template("books.html", books=books, query=query)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == "POST":
        try:
            title = require_non_empty(request.form.get("title"), "Title")
            author = require_non_empty(request.form.get("author"), "Author")
            isbn = request.form.get("isbn", "").strip() or None
            quantity = require_positive_int(request.form.get("quantity", "1"), "Quantity")

            models.add_book(title, author, isbn, quantity)
            flash(f'"{title}" added to the catalog.', "success")
            return redirect(url_for("books.list_books"))
        except ValidationError as err:
            flash(str(err), "danger")
        except Exception:
            flash("Could not add book - is the ISBN already in use?", "danger")
    return render_template("book_form.html", book=None)


@bp.route("/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
def edit_book(book_id):
    book = models.get_book(book_id)
    if book is None:
        flash("Book not found.", "danger")
        return redirect(url_for("books.list_books"))

    if request.method == "POST":
        try:
            title = require_non_empty(request.form.get("title"), "Title")
            author = require_non_empty(request.form.get("author"), "Author")
            isbn = request.form.get("isbn", "").strip() or None
            quantity = require_positive_int(request.form.get("quantity", "1"), "Quantity")

            models.update_book(book_id, title, author, isbn, quantity)
            flash("Book updated.", "success")
            return redirect(url_for("books.list_books"))
        except ValidationError as err:
            flash(str(err), "danger")
    return render_template("book_form.html", book=book)


@bp.route("/<int:book_id>/remove", methods=["POST"])
@login_required
def remove_book(book_id):
    if models.remove_book(book_id):
        flash("Book removed.", "success")
    else:
        flash("Book not found.", "danger")
    return redirect(url_for("books.list_books"))
