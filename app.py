from flask import Flask, render_template, redirect, url_for, request
from models.note import Note
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///noted.db'
db = SQLAlchemy(app)

#homepage route
@app.route('/')
def home():
    return render_template('home.html')

# Route to view all notes
@app.route('/notes')
def view_notes():
    notes = Note.query.all()
    return render_template('notes.html', notes=notes)

# Route to create a new note
@app.route('/notes/new', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_note = Note(title=title, content=content)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('view_notes'))
    return render_template('create_note.html')

# Route to edit a note
@app.route('/notes/<int:id>/edit', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get(id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        return redirect(url_for('view_notes'))
    return render_template('edit_note.html', note=note)

# Route to delete a note
@app.route('/notes/<int:id>/delete', methods=['POST'])
def delete_note(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('view_notes'))
if __name__ == '__main__':
    app.run(debug=True)