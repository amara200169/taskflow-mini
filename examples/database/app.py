"""Optional persistent TaskFlow example: SQLite locally, PostgreSQL on RDS.

Run from examples/database after installing its requirements.
Set DATABASE_URL for PostgreSQL; otherwise a local SQLite file is used.
This is a learning demo, not a secure production multi-tenant SaaS.
"""
import os
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# For PostgreSQL: postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME
# The optional query string ?sslmode=require enforces encrypted connections.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///taskflow.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)


# Creates the table if missing. For later schema changes, use migrations.
with app.app_context():
    db.create_all()


@app.get("/")
def home():
    tasks = db.session.execute(db.select(Task).order_by(Task.id)).scalars().all()
    return render_template("index.html", tasks=tasks)


@app.get("/health")
def health():
    # This checks Flask, not necessarily the database connection.
    return {"status": "ok"}


@app.post("/add")
def add_task():
    title = request.form.get("task", "").strip()
    if title:
        db.session.add(Task(title=title[:200]))
        db.session.commit()
    return redirect(url_for("home"))


@app.post("/edit/<int:task_id>")
def edit_task(task_id):
    task = db.session.get(Task, task_id)
    title = request.form.get("task", "").strip()
    if task is not None and title:
        task.title = title[:200]
        db.session.commit()
    return redirect(url_for("home"))


@app.post("/complete/<int:task_id>")
def complete_task(task_id):
    task = db.session.get(Task, task_id)
    if task is not None:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for("home"))


@app.post("/delete/<int:task_id>")
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task is not None:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
