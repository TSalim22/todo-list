# To-Do List

A task list with accounts, priorities and due dates.

## Try it in your browser

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/TSalim22/todo-list?quickstart=1)

Sign in to GitHub, open a Codespace and wait for setup. Then run this in its terminal:

```sh
python app.py
```

Open port 5000 from the **Ports** tab if the app does not open automatically.

Codespaces uses your GitHub account’s allowance. Stop it when finished.

## Run it

Python 3.12 or later. Run these commands from the project folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python app.py
```

On macOS or Linux, activate with `source .venv/bin/activate` instead.

## How to use it

Open http://127.0.0.1:5000 and create an account.

Add tasks, edit them, mark them complete or delete them. Each account has its own list. Tasks are saved in SQLite, and passwords are hashed.

## Tests

```sh
python -m pytest -q
```

## Docker (optional)

```sh
docker build -t todo-list .
docker run --rm -p 127.0.0.1:5000:5000 todo-list
```

Use a volume for saved data. Docker hasn't been tested locally.
