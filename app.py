"""TaskFlow Mini: a small Flask task manager for a practical interview demo."""

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# For this short demo, tasks live in RAM and disappear when the app restarts.
tasks = []


@app.get("/")
def home():
    # Show the current tasks in the HTML template.
    return render_template("index.html", tasks=tasks)


@app.get("/health")
def health():
    # A simple endpoint to verify the service is running.
    return {"status": "ok"}


@app.post("/add")
def add_task():
    # Read the text field named "task" from the HTML form.
    task = request.form.get("task", "").strip()
    if task:
        tasks.append(task)
    return redirect(url_for("home"))


@app.post("/delete/<int:task_id>")
def delete_task(task_id):
    # Remove a task only when its list position is valid.
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for("home"))


if __name__ == "__main__":
    # For local practice. The Dockerfile uses a production WSGI server.
    app.run(host="0.0.0.0", port=8080)
