"""Lending module: issue a book to a borrower, and process returns."""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

import models
from utils import ValidationError, login_required, require_non_empty

bp = Blueprint("loans", __name__, url_prefix="/loans")


@bp.route("/")
@login_required
def list_loans():
    return render_template(
        "loans.html",
        active_loans=models.list_active_loans(),
        overdue_loans=models.list_overdue_loans(),
    )


@bp.route("/issue", methods=["GET", "POST"])
@login_required
def issue():
    if request.method == "POST":
        try:
            book_id = int(request.form.get("book_id"))
            borrower = require_non_empty(request.form.get("borrower"), "Borrower name")

            loan_id = models.issue_book(book_id, borrower, session.get("user_id"))
            if loan_id is None:
                flash("That book is not available to issue.", "danger")
            else:
                flash(f"Book issued to {borrower}.", "success")
                return redirect(url_for("loans.list_loans"))
        except (TypeError, ValueError):
            flash("Please choose a valid book.", "danger")
        except ValidationError as err:
            flash(str(err), "danger")
    return render_template("issue_form.html", books=models.list_books())


@bp.route("/<int:loan_id>/return", methods=["POST"])
@login_required
def return_loan(loan_id):
    if models.return_book(loan_id):
        flash("Book marked as returned.", "success")
    else:
        flash("Loan not found or already returned.", "danger")
    return redirect(url_for("loans.list_loans"))
