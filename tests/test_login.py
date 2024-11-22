import unittest
from app import app, db
from models.note import Note

class LoginPageTests(unittest.TestCase):

    # Set up the test client and database
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a test database
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = app.test_client()
        with app.app_context():
            db.create_all()  # Create the tables for testing

    # Tear down the test database
    def tearDown(self):
        with app.app_context():
            db.drop_all()  # Drop the tables after the test

    # Test login page rendering
    def test_login_page_render(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    # Test successful login redirection to notes
    def test_login_redirect(self):
        # Simulate a successful login by setting a session
        with self.client:
            self.client.post('/login', data={'email': 'test@example.com', 'password': 'password'})
            response = self.client.get('/notes')
            self.assertEqual(response.status_code, 200)  # Should load the notes page

    # Test if view_notes route is accessible
    def test_view_notes(self):
        # Add a test note to the database
        note = Note(title="Test Note", content="This is a test note")
        with app.app_context():
            db.session.add(note)
            db.session.commit()

        # Request the notes page
        response = self.client.get('/notes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Note', response.data)  # Check if the note is rendered

if __name__ == '__main__':
    unittest.main()
