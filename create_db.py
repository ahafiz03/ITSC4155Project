from app import app, db  # Import your Flask app and db
from models.note import Note
from models.event import Event

def create_initial_data():
    """Function to populate the database with initial data."""
    # Example initial notes
    notes = [
        Note(title="First Note", content="This is the first note."),
        Note(title="Second Note", content="This is the second note.")
    ]

    # Example initial events
    events = [
        Event(title="Meeting", start="2024-11-23"),
        Event(title="Workshop", start="2024-11-25")
    ]

    # Add to session and commit
    db.session.add_all(notes + events)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        print("Creating database...")
        db.create_all()  # Create tables if they don't already exist
        print("Populating initial data...")
        create_initial_data()
        print("Done!")
