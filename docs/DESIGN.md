# Project Design & Layout

This document describes how the Library Management System is structured, how the web pages communicate with the database, and the layout of our database tables.

## 1. System Structure

The application follows a simple modular structure to keep our code clean and separate layout views from backend queries:
•⁠  ⁠*Frontend Pages:* Jinja2 HTML templates display the website interface and send form data via HTTP requests.
•⁠  ⁠*Route Controllers:* Flask script blueprints (⁠ auth.py ⁠, ⁠ books.py ⁠, ⁠ loans.py ⁠, ⁠ reports.py ⁠) handle URL routing and incoming user requests.
•⁠  ⁠*Validation Checkers:* ⁠ utils.py ⁠ contains basic checks to ensure fields aren't submitted blank.
•⁠  ⁠*Database Functions:* All SQL queries are gathered inside ⁠ models.py ⁠ so that we never mix raw database scripts directly inside our webpage routing code.

⁠ mermaid
flowchart TB
    subgraph Client["Client (Browser)"]
        UI[HTML Templates<br/>Jinja2 + CSS]
    end
    subgraph App["Flask Application"]
        Auth["auth.py<br/>Register / Login / Logout"]
        Books["books.py<br/>Book CRUD"]
        Loans["loans.py<br/>Issue / Return"]
        Reports["reports.py<br/>Dashboard"]
        Utils["utils.py<br/>Validation & Access Control"]
        Models["models.py<br/>Data Access Layer"]
    end
    subgraph Data["Persistence"]
        DB[("SQLite<br/>library.db")]
    end
    UI -->|HTTP requests| Auth
    UI -->|HTTP requests| Books
    UI -->|HTTP requests| Loans
    UI -->|HTTP requests| Reports
    Auth --> Utils
    Books --> Utils
    Loans --> Utils
    Auth --> Models
    Books --> Models
    Loans --> Models
    Reports --> Models
    Models --> DB
 ⁠

## 2. Program Workflow

This chart maps out the navigation choices a librarian can make once they launch the application:

⁠ mermaid
flowchart TD
    Start([Librarian opens app]) --> LoggedIn{Logged in?}
    LoggedIn -- No --> LoginPage[Login / Register]
    LoginPage --> LoggedIn
    LoggedIn -- Yes --> Dashboard[Dashboard: view stats & overdue loans]
    Dashboard --> Choice{Choose action}
    Choice --> MgBooks[Manage Books]
    Choice --> MgLoans[Manage Loans]
    MgBooks --> AddBook[Add Book]
    MgBooks --> EditBook[Edit Book]
    MgBooks --> RemoveBook[Remove Book]
    AddBook --> Validate1{Valid input?}
    Validate1 -- No --> AddBook
    Validate1 -- Yes --> SaveBook[(Save to DB)]
    SaveBook --> Dashboard
    MgLoans --> IssueBook[Issue Book to Borrower]
    MgLoans --> ReturnBook[Return Book]
    IssueBook --> Available{Copy available?}
    Available -- No --> IssueBook
    Available -- Yes --> RecordLoan[(Create loan, decrement available)]
    RecordLoan --> Dashboard
    ReturnBook --> UpdateLoan[(Mark returned, increment available)]
    UpdateLoan --> Dashboard
 ⁠

## 3. Use Case Diagram

This diagram displays what operational actions the Librarian can trigger inside the application system:

⁠ mermaid
flowchart LR
    Librarian((Librarian))
    Librarian --> UC1[Register / Log in]
    Librarian --> UC2[Add Book]
    Librarian --> UC3[Edit Book]
    Librarian --> UC4[Remove Book]
    Librarian --> UC5[Search / View Catalog]
    Librarian --> UC6[Issue Book to Borrower]
    Librarian --> UC7[Return Book]
    Librarian --> UC8[View Dashboard & Overdue Report]
 ⁠

## 4. Code Component Layout

This section tracks the data fields used within our system tables and how our database functions map into our data layouts:

⁠ mermaid
classDiagram
    class User {
        +int id
        +str username
        +str password_hash
        +str role
    }
    class Book {
        +int id
        +str title
        +str author
        +str isbn
        +int quantity
        +int available
    }
    class Loan {
        +int id
        +int book_id
        +str borrower
        +int issued_by
        +date issue_date
        +date due_date
        +date return_date
        +str status
    }
    class ModelsModule {
        +create_user()
        +add_book()
        +update_book()
        +remove_book()
        +issue_book()
        +return_book()
        +get_summary_stats()
    }
    User "1" --> "0..*" Loan : issues
    Book "1" --> "0..*" Loan : borrowed as
    ModelsModule ..> User : reads/writes
    ModelsModule ..> Book : reads/writes
    ModelsModule ..> Loan : reads/writes
 ⁠

## 5. System Execution Sequence (Book Issuing Process)

This sequence map traces exactly how data flows across files step-by-step when a librarian chooses to issue a book to a user:

⁠ mermaid
sequenceDiagram
    actor L as Librarian
    participant UI as Browser
    participant R as loans.py (Flask route)
    participant M as models.py
    participant DB as SQLite
    L->>UI: Select book, enter borrower, submit
    UI->>R: POST /loans/issue
    R->>M: issue_book(book_id, borrower, user_id)
    M->>DB: SELECT book WHERE id = ?
    DB-->>M: book row (available count)
    alt available < 1
        M-->>R: None
        R-->>UI: Flash "not available"
    else available >= 1
        M->>DB: UPDATE books SET available = available - 1
        M->>DB: INSERT INTO loans (...)
        DB-->>M: new loan id
        M-->>R: loan_id
        R-->>UI: Redirect to /loans/ with success message
    end
    UI-->>L: Show updated loan list
 ⁠

## 6. Database ER Diagram & Table Connections

Our tables are linked using IDs. One user account can handle multiple active book transactions, and one distinct book item line can be tied to several historic or current loans.

⁠ mermaid
erDiagram
    USERS ||--o{ LOANS : issues
    BOOKS ||--o{ LOANS : "is loaned as"
    USERS {
        int id PK
        string username
        string password_hash
        string role
    }
    BOOKS {
        int id PK
        string title
        string author
        string isbn
        int quantity
        int available
    }
    LOANS {
        int id PK
        int book_id FK
        string borrower
        int issued_by FK
        date issue_date
        date due_date
        date return_date
        string status
    }
 ⁠

The matching code properties and constraints can be reviewed inside our main ⁠ schema.sql ⁠ installation file.

## System Features and Rules

| Feature Area | Implementation details |
|---|---|
| *Security Guard* | User passwords are encrypted with mathematical salts using ⁠ werkzeug.security ⁠. Pages are locked behind a custom ⁠ login_required ⁠ session gate so external users can't bypass authentication. |
| *Data Safety* | Library inventory details sit safely inside an SQLite database instead of local running memory arrays, ensuring no data wipes out if the web app restarts. |
| *Usability Design* | The web view features a clean, simple styling layout with flash banner notifications that give instant visual feedback if an action succeeds or fails. |
| *Error Protections* | Includes custom 404 and 500 error landing handlers to prevent raw Python system traces from rendering on user windows during an application glitch. |
| *Search Speed* | Added field sorting parameters and direct table indices on structural search categories like ⁠ books.title ⁠ and ⁠ loans.status ⁠ to keep query lookup swift. |