# Optional Database Integration — TaskFlow

**Your original root-level `app.py` stays unchanged.** Use it for the 60-minute interview. This directory is an optional reference for adding persistence later.

## 1. Understand the change

- In the original app, `tasks = []` stores data in process memory. Restarting Flask loses the tasks.
- In this example, `Task` is a SQLAlchemy database model with `id`, `title`, and `completed`.
- `db.session.add(...)` inserts a row, `db.session.commit()` saves a transaction, and `db.session.delete(...)` removes a row.
- Flask's HTML form still handles each button, so no JavaScript is required.
- `DATABASE_URL` chooses the database without hard-coding passwords.
- The app creates its `task` table with `db.create_all()` on startup. This **does not migrate existing tables or copy in-memory tasks**.

Architecture:

```text
Browser -> Flask HTML forms -> Flask routes -> SQLAlchemy -> SQLite file
                                                    \-> PostgreSQL / RDS
```

## 2. Fastest local database: SQLite (Windows PowerShell)

From the root of the cloned repository:

```powershell
# Move into the optional database example
cd examples/database

# Make a separate Python environment
py -m venv .venv

# Install Flask + SQLAlchemy + PostgreSQL driver
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Start the optional database version; defaults to SQLite
.\.venv\Scripts\python.exe app.py
```

Open **http://127.0.0.1:8080**. Add a task, edit its title, mark it complete, and delete it.

**Verify persistence:** Add a harmless sample task, stop the server with Ctrl+C, restart using the same command, and refresh. The task should still be present. SQLite's database file is created under Flask's **instance directory** (typically `examples/database/instance/taskflow.db`).

**Check SQLite content without adding tools:**

```powershell
# From examples/database
.\.venv\Scripts\python.exe -c "import sqlite3; c=sqlite3.connect('instance/taskflow.db'); print(c.execute('SELECT id, title, completed FROM task').fetchall()); c.close()"
```

**Undo only your optional practice database:** Stop the application. Make a backup of `instance/taskflow.db` if you want the tasks; only then delete that file. Deleting the SQLite file permanently removes those saved tasks.

## 3. Connect PostgreSQL locally or Amazon RDS

**Do not replace the original `app.py` during the timed interview.** The steps below are optional.

First, provision a PostgreSQL database you control. For Amazon RDS, you need:

- PostgreSQL DB instance, hostname (endpoint), port (usually **5432**), a database name, and an authorized database user.
- An EC2 instance / client that can reach the DB. Prefer **private RDS** and allow inbound port 5432 **only from the application EC2 security group**, not from `0.0.0.0/0`.
- The application security group must permit the necessary outbound traffic. Your VPC route tables and NACLs must also allow the connection.
- TLS according to your deployment requirements (for a basic PostgreSQL connection, `sslmode=require` encrypts the connection but does not by itself validate the server's identity; for strong identity verification use `sslmode=verify-full` with the appropriate trusted CA certificate).
- Use AWS Secrets Manager or another approved secret store in a real deployment. Never commit DB passwords or AWS credentials to GitHub.

### Environment variable

Set `DATABASE_URL` for the app process. This is the only configuration change required by this example.

In **PowerShell** (enter a real value only in a safe environment; avoid putting production credentials into shell history):

```powershell
# Example only: replace all placeholders with your own database details.
# URI-encode special characters in USER or PASSWORD.
$env:DATABASE_URL = "postgresql+psycopg://USER:PASSWORD@YOUR_RDS_ENDPOINT:5432/taskflow?sslmode=require"

# Run the optional database example
.\.venv\Scripts\python.exe app.py
```

On **Linux**, prefer injecting the environment variable via a properly secured secret store or process manager; if testing with dummy local credentials:

```bash
export DATABASE_URL='postgresql+psycopg://USER:PASSWORD@DB_HOST:5432/taskflow?sslmode=require'
python app.py
```

The application reads this value using:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///taskflow.db"
)
```

- When `DATABASE_URL` is unset, it uses SQLite.
- When set to the PostgreSQL connection string, it uses PostgreSQL.
- `db.create_all()` creates the missing table on the selected database.

**Security:** Never paste real passwords into ChatGPT, screenshots, code, public GitHub repos, or a committed `.env` file. A public frontend is **not** a reason to expose PostgreSQL to the internet. Keep the DB private.

## 4. Test database access without making changes

If PostgreSQL's `psql` client is installed, check connectivity with:

```bash
# Adjust host, username, and database; use a secure password prompt.
psql "host=YOUR_RDS_ENDPOINT port=5432 dbname=taskflow user=YOUR_DB_USER sslmode=require" -c "SELECT 1;"
```

Only after the connectivity check, start Flask and add a sample task through the webpage.

To verify stored tasks in PostgreSQL:

```sql
SELECT id, title, completed FROM task ORDER BY id;
```

This is a **read-only** verification query.

## 5. Common errors and fixes

| Symptom | Likely cause | Check |
| --- | --- | --- |
| Connection timed out | Wrong endpoint, security group, route, or NACL | Validate private connectivity to RDS:5432 |
| Authentication failed | Wrong credentials or DB user | Verify the secret and user permissions |
| Database does not exist | Wrong DB name | Check RDS databases / connection string |
| SSL error | TLS configuration or certificate mismatch | Review sslmode and trusted CA |
| ModuleNotFoundError | Missing dependencies | Install `requirements.txt` into the running environment |
| Tasks disappear after restart | Running root `app.py`, not database example | Confirm current working directory and application file |
| Port already in use | Another local app uses 8080 | Stop conflicting service or change local bind port |

## 6. Rollback and costs

- **Switch back to the minimal interview app:** stop the database example; from the repository root run `python app.py`. This does not delete saved database rows.
- **Switch the optional example back to SQLite:** remove `DATABASE_URL` for that shell session: `Remove-Item Env:DATABASE_URL` in PowerShell (or `unset DATABASE_URL` in Bash). This does **not** migrate PostgreSQL records into SQLite.
- Do not drop RDS databases or delete tables as part of troubleshooting.
- AWS RDS and associated resources may incur charges even while idle. Review pricing and remove **unused resources** only when you intentionally no longer need them, after confirming backups.

## 7. Interview explanation (short)

> "The one-hour demo uses an in-memory list to keep the scope small. If persistence were required, I would replace that list with a SQLAlchemy Task model. Locally I'd use SQLite; in AWS I'd set DATABASE_URL to a private PostgreSQL RDS endpoint, allow database traffic only from the EC2 security group, keep credentials in Secrets Manager, and verify the data survives application restarts."

**One-hour recommendation:** Focus on the root app. Treat this folder as an optional extension/reference if the interviewer asks about a database.
