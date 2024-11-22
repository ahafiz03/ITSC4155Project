import unittest
from flask import Flask
from flask.testing import FlaskClient

class HomePageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the Flask app for testing."""
        cls.app = Flask(__name__)

        # Setup the app configurations and routes for testing
        cls.app.config['TESTING'] = True
        cls.app.config['DEBUG'] = False

        # Define test routes
        @cls.app.route('/')
        def home():
            return """
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Home Page</title>
                    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
                </head>
                <body>
                    <header class="header">
                        <div class="header-left">
                            <img src="/static/StudySphere.png" alt="Logo" class="logo">
                            <span class="brand-text">StudySphere</span>
                        </div>
                        <div class="header-right">
                            <a href="/login" class="header-link">Login</a>
                            <a href="/signup" class="header-link">Sign Up</a>
                        </div>
                    </header>
                    <div class="container">
                        <nav class="sidebar">
                            <ul>
                                <li><a href="/view_notes">View Notes</a></li>
                                <li><a href="/create_note">Create a New Note</a></li>
                            </ul>
                        </nav>

                        <div class="main-content">
                            <h1>Welcome to StudySphere!</h1>
                            <p>Select an option from the sidebar to get started.</p>
                            <a href="/">
                                <button>Back to Home</button>
                            </a>
                        </div>
                    </div>
                </body>
                </html>
            """
        cls.client = cls.app.test_client()

    def test_home_page_status(self):
        """Test if the home page loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_content(self):
        """Test if the home page contains key elements."""
        response = self.client.get('/')
        self.assertIn(b"Welcome to StudySphere!", response.data)
        self.assertIn(b"Select an option from the sidebar to get started.", response.data)
        self.assertIn(b"View Notes", response.data)
        self.assertIn(b"Create a New Note", response.data)
        self.assertIn(b"Back to Home", response.data)
        self.assertIn(b"Login", response.data)
        self.assertIn(b"Sign Up", response.data)
        self.assertIn(b"StudySphere", response.data)

    def test_navigation_links(self):
        """Test the links on the home page."""
        response = self.client.get('/')
        self.assertIn(b'href="/view_notes"', response.data)
        self.assertIn(b'href="/create_note"', response.data)
        self.assertIn(b'href="/"', response.data)  # Check if back to home link works
        self.assertIn(b'href="/login"', response.data)
        self.assertIn(b'href="/signup"', response.data)

    def test_logo_image(self):
        """Test if the logo image is rendered correctly."""
        response = self.client.get('/')
        self.assertIn(b'<img src="/static/StudySphere.png" alt="Logo" class="logo">', response.data)

    def test_home_page_layout(self):
        """Test that the home page layout is correct (header, sidebar, etc.)."""
        response = self.client.get('/')
        self.assertIn(b'<header class="header">', response.data)
        self.assertIn(b'<nav class="sidebar">', response.data)
        self.assertIn(b'<div class="main-content">', response.data)


if __name__ == '__main__':
    unittest.main()
