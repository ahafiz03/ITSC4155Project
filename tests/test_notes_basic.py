import unittest
from app import app, db  # Use the existing app and db instances
from models.note import Note

class NoteModelTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the database before each test.
        """
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Drop all tables after each test to ensure isolation.
        """
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_note(self):
        """
        Test creating a note.
        """
        with app.app_context():
            # Add the note
            note = Note(title="Test Note", content="This is a test note.")
            db.session.add(note)
            db.session.commit()

            # Retrieve the note
            retrieved_note = Note.query.first()

            # Assertions
            self.assertIsNotNone(retrieved_note)
            self.assertEqual(retrieved_note.title, "Test Note")  # Ensure correct title
            self.assertEqual(retrieved_note.content, "This is a test note.")  # Ensure correct content

    def test_update_note(self):
        """
        Test updating an existing note.
        """
        with app.app_context():
            note = Note(title="Old Note", content="This is an old note.")
            db.session.add(note)
            db.session.commit()

            # Update the note
            note.title = "Updated Note"
            note.content = "This note has been updated."
            db.session.commit()

            updated_note = Note.query.get(note.id)
            self.assertEqual(updated_note.title, "Updated Note")
            self.assertEqual(updated_note.content, "This note has been updated.")

    def test_delete_note(self):
        """
        Test deleting a note.
        """
        with app.app_context():
            note = Note(title="Note to Delete", content="This note will be deleted.")
            db.session.add(note)
            db.session.commit()

            # Delete the note
            db.session.delete(note)
            db.session.commit()

            deleted_note = Note.query.get(note.id)
            self.assertIsNone(deleted_note)

    def test_retrieve_all_notes(self):
        """
        Test retrieving all notes.
        """
        with app.app_context():
            # Add multiple notes
            note1 = Note(title="Note 1", content="Content for note 1")
            note2 = Note(title="Note 2", content="Content for note 2")
            db.session.add_all([note1, note2])
            db.session.commit()

            all_notes = Note.query.all()
            self.assertEqual(len(all_notes), 2)
            self.assertEqual(all_notes[0].title, "Note 1")
            self.assertEqual(all_notes[1].title, "Note 2")

if __name__ == '__main__':
    unittest.main()
