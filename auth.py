"""Authentication module: registration, login, logout.

Passwords are never stored or compared in plain text - werkzeug's
generate_password_hash / check_password_hash (PBKDF2) are used instead.
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import models
from utils import ValidationError, require_non_empty

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            username = require_non_empty(request.form.get("username"), "Username")
            password = require_non_empty(request.form.get("password"), "Password")
            if len(password) < 6:
                raise ValidationError("Password must be at least 6 characters.")
            if models.get_user_by_username(username) is not None:
                raise ValidationError("That username is already taken.")

            models.create_user(username, generate_password_hash(password))
            flash("Account created. Please log in.", "success")
            return redirect(url_for("auth.login"))
        except ValidationError as err:
            flash(str(err), "danger")
    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = models.get_user_by_username(username)

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.", "danger")
        else:
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for("reports.dashboard"))
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
