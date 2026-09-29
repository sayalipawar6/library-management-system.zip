-- Library Management System schema

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL DEFAULT 'librarian' CHECK (role IN ('librarian', 'member')),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS books (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    author      TEXT NOT NULL,
    isbn        TEXT UNIQUE,
    quantity    INTEGER NOT NULL DEFAULT 1 CHECK (quantity >= 0),
    available   INTEGER NOT NULL DEFAULT 1 CHECK (available >= 0),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loans (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id     INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    borrower    TEXT NOT NULL,
    issued_by   INTEGER REFERENCES users(id),
    issue_date  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date    DATE NOT NULL,
    return_date TIMESTAMP,
    status      TEXT NOT NULL DEFAULT 'issued' CHECK (status IN ('issued', 'returned', 'overdue'))
);

CREATE INDEX IF NOT EXISTS idx_loans_book_id ON loans(book_id);
CREATE INDEX IF NOT EXISTS idx_loans_status ON loans(status);
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
