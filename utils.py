"""Shared validation helpers and decorators (error handling / access control)."""
from functools import wraps

from flask import flash, redirect, session, url_for


class ValidationError(Exception):
    """Raised when user-submitted data fails validation."""


def require_non_empty(value, field_name):
    if value is None or not str(value).strip():
        raise ValidationError(f"{field_name} is required.")
    return str(value).strip()


def require_positive_int(value, field_name):
    try:
        n = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} must be a whole number.")
    if n < 0:
        raise ValidationError(f"{field_name} cannot be negative.")
    return n


def login_required(view):
    """Redirect anonymous users to the login page."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped
