import unittest
import json
from app import app, db, Event  # Import the Flask app, database, and Event model

class FlaskAppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_events.db'
        app.config['TESTING'] = True
        cls.client = app.test_client()

        with app.app_context():
            db.create_all()  # Create tables

    @classmethod
    def tearDownClass(cls):
        # Clean up the test database
        with app.app_context():
            db.drop_all()

    def setUp(self):
        # Set up initial data
        self.client = self.__class__.client
        self.event_data = {'title': 'Test Event', 'start': '2023-12-31'}

    def test_add_event(self):
        response = self.client.post('/add_event', data=json.dumps(self.event_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

        # Verify the event was added
        with app.app_context():
            event = Event.query.filter_by(title='Test Event').first()
            self.assertIsNotNone(event)
            self.assertEqual(event.start, '2023-12-31')

    def test_get_events(self):
        # Add an event first
        self.client.post('/add_event', data=json.dumps(self.event_data), content_type='application/json')

        response = self.client.get('/get_events')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(any(event['title'] == 'Test Event' for event in data))

    def test_delete_event(self):
        # Add an event first
        self.client.post('/add_event', data=json.dumps(self.event_data), content_type='application/json')

        # Get the event ID
        with app.app_context():
            event = Event.query.filter_by(title='Test Event').first()
            event_id = event.id

        # Delete the event
        response = self.client.delete(f'/delete_event/{event_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

        # Verify the event was deleted
        with app.app_context():
            event = Event.query.get(event_id)
            self.assertIsNone(event)

if __name__ == "__main__":
    unittest.main()
