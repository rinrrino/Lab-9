app.py
`python
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    important = db.Column(db.Boolean, default=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    notes = Note.query.order_by(Note.id.desc()).all()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add():
    text = request.form.get('text','').strip()
    important = bool(request.form.get('important'))
    if text:
        n = Note(text=text, important=important)
        db.session.add(n)
        db.session.commit()
    return redirect(url_for('index'))

# minimal templates: templates/index.html
if name == 'main':
    app.run(debug=True)
