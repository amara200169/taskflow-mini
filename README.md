# TaskFlow Mini

A tiny **clickable task-management web app** built with Flask and HTML forms for an interview practice demo. Visitors can **add, view, and delete tasks** from a browser without JavaScript or terminal commands.

**Limitations:** All tasks are stored in Python memory, so a process restart clears them. One worker is used to keep the single list consistent in this demo. There are no user accounts or authentication: anyone with access to the site can change its tasks. **Use dummy tasks only; do not use it as a production or public multi-user service.**

## Project files

- `app.py` — Flask routes and temporary task storage
- `templates/index.html` — HTML dashboard and forms, with small inline CSS
- `requirements.txt` — Python dependencies
- `Dockerfile` — optional container packaging
- `tests/test_app.py` — automated local checks

## Run without Docker (Windows PowerShell)

Open PowerShell inside the `taskflow-mini` folder:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe app.py
```

Open http://localhost:8080 for the dashboard and http://localhost:8080/health for the health check. Using the environment's Python executable directly avoids changing PowerShell execution policies.

## Run with Docker (optional)

```bash
docker build -t taskflow-mini .
docker run --name taskflow-mini -d -p 8080:8080 taskflow-mini
docker ps
docker logs taskflow-mini
```

Open http://localhost:8080 and http://localhost:8080/health.

To stop without removing:

```bash
docker stop taskflow-mini
```

The data is temporary. Stopping/restarting the application loses any tasks kept in RAM.

## Clone from GitHub

```bash
git clone https://github.com/amara200169/taskflow-mini.git
cd taskflow-mini
```

If private, the repository requires authorized GitHub access.

## cURL fallback — if you skip the HTML buttons during the interview

The root application already accepts **HTML form submissions**, so these commands work without a clickable UI. They use the existing Flask routes in `app.py`, **not** the JSON routes from the separate API practice exercise.

Run these commands in **Git Bash, Linux, or macOS Terminal** after starting the app.

### 1. Confirm the service is healthy (read-only)

```bash
curl -i http://localhost:8080/health
```

Expected response body: `{"status":"ok"}`.

### 2. Create a task

```bash
# -d submits the same form field (name="task") as the webpage.
# -i shows the HTTP response headers; the app redirects to / after creating.
curl -i -X POST http://localhost:8080/add -d "task=Learn AWS"
```

The app replies with a redirect to `/`. Follow it to view your saved task:

```bash
curl -L -X GET http://localhost:8080/
```

Or open `http://localhost:8080/` in a browser.

### 3. Delete the task

```bash
# Delete the task at zero-based list position 0 (the first task).
# WARNING: This changes in-memory data; double-check the index.
curl -i -X POST http://localhost:8080/delete/0
```

Confirm by opening `http://localhost:8080/` again (or run `curl http://localhost:8080/`). There is no undo other than adding the task again. When a task is deleted, the remaining task positions shift.

**If deploying to AWS:** replace `http://localhost:8080` with your actual service URL and port. For example, when host port 80 maps to container port 8080, use `http://YOUR_PUBLIC_IP` without `:8080`. Do not assume an existing instance IP will be provided for the coding test.

**Important:** This repo uses `POST /add` with the form field `task`, and `POST /delete/<index>`. It does **not** use `POST /tasks` with JSON or `DELETE /tasks/<id>`. If you build the separate JSON API from memory instead, the cURL commands must match those different routes and request formats.

## Troubleshooting

- If `py` is missing, install Python for Windows or use your installed Python executable.
- If port 8080 is already used, stop the conflicting application or change both the Flask port and browser URL.
- If the page renders but tasks disappear after restart, that's expected: storage is in RAM.
- If Flask imports fail, install the requirements using the same Python executable you use to run the app.

## Interview note

Ask whether reusing previously written code is allowed before cloning it during the assessment. The instructions shown do not explicitly confirm permission to submit a prebuilt application.

## Optional database upgrade (not needed for the timed interview)

See [examples/database/README.md](examples/database/README.md) for a separate, working Flask + SQLAlchemy version with SQLite locally, an optional private PostgreSQL/RDS connection through `DATABASE_URL`, HTML edit/complete/delete buttons, safe connection guidance, and verification steps. The original root-level app stays unchanged.
