from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from extensions import db  # Import the db from extensions
from models.note import Note
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///noted.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'


db.init_app(app)  # Initialize db with the app
migrate = Migrate(app, db)  # Initialize Migrate
# Creates the event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start = db.Column(db.String(10), nullable=False)

# Homepage route
@app.route('/')
def home():
    return render_template('home.html')

# Route to view all notes
@app.route('/notes')
def view_notes():
    notes = Note.query.order_by(Note.last_modified.desc()).all()
    return render_template('notebook.html', notes=notes)

# Route to create a new note
@app.route('/notes/new', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_note = Note(title=title, content=content)
        db.session.add(new_note)
        db.session.commit()
        flash('Note created successfully!', 'success')
        return redirect(url_for('view_notes'))
    return render_template('create_note.html')

# Route to edit a note
@app.route('/notes/<int:id>/edit', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        flash('Note updated successfully!', 'success')
        return redirect(url_for('view_notes'))
    return render_template('edit_note.html', note=note)

# Route to delete a note
@app.route('/notes/<int:id>/delete', methods=['POST'])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully!', 'danger')
    return redirect(url_for('view_notes'))

# Route to render calendar
@app.route('/calendar')
def index():
    return render_template('calendar.html')

# Route to view events
@app.route('/get_events')
def get_events():
    events = Event.query.all()
    event_list = [{'title': event.title, 'start': event.start} for event in events]
    return jsonify(event_list)

# Route to add event to calendar
@app.route('/add_event', methods=['POST'])
def add_event():
    event_data = request.json
    new_event = Event(title=event_data['title'], start=event_data['start'])
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'success': True})

# Route to delete an event 
@app.route('/delete_event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Event not found'}), 404

# Route to create an account
@app.get("/signup")
def get_account_signup_page():
    if "email" in session:
        return redirect("/account")
    return render_template("signup.html")

# Route to login to account
@app.get("/login")
def get_account_login_page():
    if "email" in session:
        return redirect("/account")
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
