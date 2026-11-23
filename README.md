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

## Troubleshooting

- If `py` is missing, install Python for Windows or use your installed Python executable.
- If port 8080 is already used, stop the conflicting application or change both the Flask port and browser URL.
- If the page renders but tasks disappear after restart, that's expected: storage is in RAM.
- If Flask imports fail, install the requirements using the same Python executable you use to run the app.

## Interview note

Ask whether reusing previously written code is allowed before cloning it during the assessment. The instructions shown do not explicitly confirm permission to submit a prebuilt application.
