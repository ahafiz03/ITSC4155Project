import unittest
from flask import Flask, render_template_string
from flask.testing import FlaskClient

class SignupPageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the Flask app for testing."""
        cls.app = Flask(__name__)

        # Set app configurations
        cls.app.config['TESTING'] = True
        cls.app.config['DEBUG'] = False

        # Define test routes
        @cls.app.route('/signup', methods=['POST', 'GET'])
        def signup():
            return render_template_string("""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Sign Up</title>
                    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
                </head>
                <body>
                    <header class="header">
                        <div class="header-left">
                            <img src="/static/StudySphere.png" alt="Logo" class="logo">
                            <span class="brand-text">StudySphere</span>
                        </div>
                        <div class="header-right">
                            <a href="{{ url_for('login') }}" class="header-link">Login</a>
                            <a href="{{ url_for('signup') }}" class="header-link">Sign Up</a>
                        </div>
                    </header>
                    <div class="container">
                        <div class="sidebar">
                            <ul>
                                <li><a href="{{ url_for('view_notes') }}">View Notes</a></li>
                                <li><a href="{{ url_for('home') }}">Back to Home</a></li>
                                <li><a href="{{ url_for('create_note') }}">Create a New Note</a></li>
                            </ul>
                        </div>
                        <div class="main-content">
                            <div class="form-container">
                                <h1 class="text-center">Sign Up</h1>
                                <form action="/signup" method="POST" class="note-form">
                                    <div class="form-group">
                                        <label for="first_name">First Name</label>
                                        <input type="text" class="form-control" name="first_name" id="first_name" placeholder="Enter First Name" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="last_name">Last Name</label>
                                        <input type="text" class="form-control" name="last_name" id="last_name" placeholder="Enter Last Name" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="email">Email</label>
                                        <input type="email" class="form-control" name="email" id="email" placeholder="Enter email" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="password">Password</label>
                                        <input type="password" class="form-control" name="password" id="password" placeholder="Password" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="re-password">Re-enter Password</label>
                                        <input type="password" class="form-control" name="re-password" id="re-password" placeholder="Re-enter Password" required>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Sign Up</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </body>
                </html>
            """)

        @cls.app.route('/login')
        def login():
            return 'Login Page'

        @cls.app.route('/home')
        def home():
            return 'Home Page'

        @cls.app.route('/view_notes')
        def view_notes():
            return 'View Notes'

        @cls.app.route('/create_note')
        def create_note():
            return 'Create Note'

        cls.client = cls.app.test_client()

    def test_signup_page_render(self):
        """Test if the signup page renders successfully."""
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_form_fields(self):
        """Test if the signup form has the required input fields."""
        response = self.client.get('/signup')

        # Check if form fields exist
        self.assertIn(b'<input type="text" class="form-control" name="first_name"', response.data)
        self.assertIn(b'<input type="text" class="form-control" name="last_name"', response.data)
        self.assertIn(b'<input type="email" class="form-control" name="email"', response.data)
        self.assertIn(b'<input type="password" class="form-control" name="password"', response.data)
        self.assertIn(b'<input type="password" class="form-control" name="re-password"', response.data)

    def test_submit_button(self):
        """Test if the signup form has a submit button."""
        response = self.client.get('/signup')
        self.assertIn(b'<button type="submit" class="btn btn-primary">Sign Up</button>', response.data)

    def test_signup_page_links(self):
        """Test if the signup page has links to login and home."""
        response = self.client.get('/signup')
        self.assertIn(b'href="/login"', response.data)
        self.assertIn(b'href="/home"', response.data)

if __name__ == '__main__':
    unittest.main()
