# Unit testing file to verify our app works before deployment.
# Run command: python -m unittest discover -s tests -v
#
# Note: This creates a temporary SQLite file for testing so it doesn't
# overwrite or mess up our actual library.db entries.
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app  # noqa: E402
from config import TestConfig  # noqa: E402


class LibraryTestCase(unittest.TestCase):
    
    # This runs automatically before every single test function below
    def setUp(self):
        # Create a blank temporary database file path
        self.db_fd, db_path = tempfile.mkstemp()

        class CaseConfig(TestConfig):
            DATABASE_PATH = db_path

        # Setup an isolated test app instance and test client
        self.app = create_app(CaseConfig)
        self.client = self.app.test_client()

    # This cleans up the files after the tests complete
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.app.config["DATABASE_PATH"])

    # Shortcut function to handle login quickly inside tests
    def register_and_login(self, username="alice", password="secret123"):
        self.client.post(
            "/auth/register", data={"username": username, "password": password}
        )
        return self.client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    # --- Authentication Route Tests ---
    def test_register_and_login_success(self):
        resp = self.register_and_login()
        self.assertEqual(resp.status_code, 302)  # Check for redirect to dashboard

    def test_login_with_wrong_password_fails(self):
        self.client.post(
            "/auth/register", data={"username": "bob", "password": "correctpass"}
        )
        resp = self.client.post(
            "/auth/login", data={"username": "bob", "password": "wrongpass"},
            follow_redirects=True,
        )
        self.assertIn(b"Invalid username or password", resp.data)

    def test_short_password_rejected(self):
        resp = self.client.post(
            "/auth/register", data={"username": "carol", "password": "123"},
            follow_redirects=True,
        )
        self.assertIn(b"at least 6 characters", resp.data)

    def test_duplicate_username_rejected(self):
        self.client.post(
            "/auth/register", data={"username": "dave", "password": "secret123"}
        )
        resp = self.client.post(
            "/auth/register", data={"username": "dave", "password": "secret123"},
            follow_redirects=True,
        )
        self.assertIn(b"already taken", resp.data)

    def test_dashboard_requires_login(self):
        resp = self.client.get("/", follow_redirects=True)
        self.assertIn(b"Log in", resp.data)

    # --- Book Management System Tests ---
    def test_add_book_requires_login(self):
        resp = self.client.get("/books/add", follow_redirects=True)
        self.assertIn(b"Please log in", resp.data)

    def test_add_and_list_book(self):
        self.register_and_login()
        self.client.post(
            "/books/add",
            data={"title": "Clean Code", "author": "Robert Martin", "isbn": "", "quantity": "3"},
        )
        resp = self.client.get("/books/")
        self.assertIn(b"Clean Code", resp.data)
        self.assertIn(b"3 / 3", resp.data)

    def test_add_book_requires_title(self):
        self.register_and_login()
        resp = self.client.post(
            "/books/add",
            data={"title": "", "author": "Someone", "quantity": "1"},
            follow_redirects=True,
        )
        self.assertIn(b"Title is required", resp.data)

    def test_remove_book(self):
        self.register_and_login()
        self.client.post(
            "/books/add", data={"title": "Temp Book", "author": "X", "quantity": "1"}
        )
        resp = self.client.get("/books/")
        book_id = self._extract_first_id(resp.data)
        self.client.post(f"/books/{book_id}/remove")
        resp = self.client.get("/books/")
        self.assertNotIn(b"Temp Book", resp.data)

    # --- Circulation / Loan Process Tests ---
    def test_issue_and_return_book(self):
        self.register_and_login()
        self.client.post(
            "/books/add", data={"title": "Dune", "author": "Frank Herbert", "quantity": "1"}
        )
        book_id = self._extract_first_id(self.client.get("/books/").data)

        resp = self.client.post(
            "/loans/issue", data={"book_id": book_id, "borrower": "Jordan"},
            follow_redirects=True,
        )
        self.assertIn(b"Book issued to Jordan", resp.data)

        # Confirm stock levels updated instantly
        resp = self.client.get("/books/")
        self.assertIn(b"0 / 1", resp.data)

        loan_id = self._extract_first_id(self.client.get("/loans/").data)
        resp = self.client.post(f"/loans/{loan_id}/return", follow_redirects=True)
        self.assertIn(b"marked as returned", resp.data)

        resp = self.client.get("/books/")
        self.assertIn(b"1 / 1", resp.data)

    def test_cannot_issue_unavailable_book(self):
        self.register_and_login()
        self.client.post(
            "/books/add", data={"title": "Rare Book", "author": "Y", "quantity": "1"}
        )
        book_id = self._extract_first_id(self.client.get("/books/").data)
        self.client.post("/loans/issue", data={"book_id": book_id, "borrower": "A"})
        resp = self.client.post(
            "/loans/issue", data={"book_id": book_id, "borrower": "B"},
            follow_redirects=True,
        )
        self.assertIn(b"not available to issue", resp.data)

    # --- Custom Helpers for HTML Parsing ---
    @staticmethod
    def _extract_first_id(html_bytes):
        # Scan HTML text using regex to grab the dynamic database ID from the link string
        import re
        match = re.search(rb"/(?:books|loans)/(\d+)/", html_bytes)
        return int(match.group(1)) if match else None


if __name__ == "_main_":
    unittest.main()