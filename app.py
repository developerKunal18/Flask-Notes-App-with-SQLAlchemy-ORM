from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ---------- Database Config ----------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------- Model ----------
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

# Create DB
with app.app_context():
    db.create_all()

# ---------- Home ----------
@app.route("/")
def index():
    notes = Note.query.all()

    return render_template(
        "index.html",
        notes=notes
    )

# ---------- Add ----------
@app.route("/add", methods=["POST"])
def add_note():
    content = request.form["content"]

    new_note = Note(content=content)

    db.session.add(new_note)
    db.session.commit()

    return redirect("/")

# ---------- Delete ----------
@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    note = Note.query.get(note_id)

    if note:
        db.session.delete(note)
        db.session.commit()

    return redirect("/")

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
