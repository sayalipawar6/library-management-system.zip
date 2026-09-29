# Library Management System

A web-based Library Management System built with **Flask** and **SQLite**,
created as a VITyarthi "Build Your Own Project" course submission.

## Overview

The system lets a librarian manage a book catalog and track lending
activity through a browser-based interface: adding/editing/removing
books, issuing books to borrowers with a due date, processing returns,
and viewing a dashboard of overdue loans and catalog statistics.

## Features

- **User management** — librarian registration and login, with hashed
  passwords (no plaintext storage) and session-based access control.
- **Book catalog (CRUD)** — add, edit, remove, and search books by
  title/author/ISBN, with per-title copy counts.
- **Lending workflow** — issue a book to a borrower (creates a loan with
  a 14-day due date and decrements available copies) and mark a loan
  as returned (increments available copies back).
- **Reporting/dashboard** — total copies, available copies, active
  loans, and an overdue-loans report.
- **Validation & error handling** — required-field checks, positive
  quantity checks, duplicate-username/ISBN handling, and friendly
  flash-message feedback instead of raw stack traces.

## Technologies / Tools Used

- Python 3, Flask 3
- SQLite (accessed directly via the `sqlite3` standard library — no ORM)
- Jinja2 templates, plain CSS
- Werkzeug's `generate_password_hash` / `check_password_hash` for auth
- `unittest` for automated testing
- Graphviz + Matplotlib for the design diagrams in `docs/diagrams/`

## Project Structure

```
library-management-system/
├── app.py              # Application factory / entry point
├── config.py           # Configuration (base + test)
├── db.py               # SQLite connection handling, schema init
├── schema.sql           # Database schema (users, books, loans)
├── models.py            # Data access layer (all SQL lives here)
├── auth.py              # Blueprint: register / login / logout
├── books.py              # Blueprint: book CRUD
├── loans.py              # Blueprint: issue / return
├── reports.py            # Blueprint: dashboard
├── utils.py              # Validation helpers + login_required decorator
├── templates/            # Jinja2 HTML templates
├── static/style.css       # Stylesheet
├── tests/test_app.py      # Automated test suite (11 tests)
├── docs/
│   ├── DESIGN.md          # Architecture, workflow, UML & ER diagrams
│   └── diagrams/          # Diagram source (.dot/.mmd) + rendered PNGs
├── statement.md
├── requirements.txt
└── README.md
```

## Steps to Install & Run

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd library-management-system

# 2. Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

The app starts at `http://127.0.0.1:5000/`. The SQLite database
(`library.db`) and its tables are created automatically on first run.
Register a librarian account, then log in.

## Instructions for Testing

The test suite uses Python's built-in `unittest` module (no extra
dependencies) and runs against a temporary, isolated SQLite file per
test so it never touches your real `library.db`.

```bash
python -m unittest discover -s tests -v
```

Expected result: 11 tests, all passing — covering registration/login
validation, book CRUD, and the full issue/return lending cycle
(including the "book not available" edge case).

## Screenshots

See `docs/diagrams/` for architecture and design diagrams. Add
screenshots of the running application here once deployed locally.

## Future Enhancements

- Member/borrower self-service accounts (currently librarian-only)
- Email/SMS due-date reminders
- Pagination for large catalogs
- CSV export for reports
# library-management-system.zip
