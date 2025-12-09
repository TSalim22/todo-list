# To-Do List

A private task list with accounts, priorities and due dates.

This is a small, independent Python portfolio project. The code favours ordinary functions and clear modules over complex architecture.

## Setup

Requires Python 3.12+ (desktop tools also require Tkinter, included with the standard Windows Python installer).

```sh
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux instead: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python app.py
```

Run commands from this repository's root. Web apps bind to localhost by default. Each app is independent, so stop one before starting another on the same port.

## Check it

```sh
python -m pytest -q
```

## Dates

The commit author dates have been deliberately arranged between October 2025 and October 2026 at the portfolio owner's request. They are presentation metadata, not a record of the actual development timeline. Repository creation and upload timestamps remain the real dates.

## Try it

Open http://127.0.0.1:5000, register an account, then add a task. Choose a priority and an optional due date. Edit, complete, reopen, delete or filter tasks from the main page. Register a second account to see that each account has its own list.

Passwords are hashed, forms use CSRF tokens, and record queries check ownership. Data is stored in `instance/project.db`, which is ignored by Git. This adapts the original cloud app to Python with a local SQL database.

## Optional local container

```sh
docker build -t todo-list .
docker run --rm -p 127.0.0.1:5000:5000 todo-list
```

This runs a local demonstration server. Container storage is temporary unless you mount a volume for `instance/`. Docker commands were supplied but Docker is not installed in the development environment, so container execution was not verified here.
