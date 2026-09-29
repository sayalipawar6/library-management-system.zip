"""Reporting module: dashboard summary statistics for librarians."""
from flask import Blueprint, render_template

import models
from utils import login_required

bp = Blueprint("reports", __name__, url_prefix="/")


@bp.route("/")
@login_required
def dashboard():
    stats = models.get_summary_stats()
    return render_template(
        "dashboard.html", stats=stats, overdue=models.list_overdue_loans()
    )
