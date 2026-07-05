# Database Carry-Forward Strategy

From this upgrade onward, keep the old `db.sqlite3` and apply new migrations to it. Do not create a fresh database unless you intentionally want a reset.

## Best daily start

Run:

```bat
start_server_windows.bat
```

This script now:

1. backs up `db.sqlite3` into `db_backups/`
2. runs `python manage.py migrate --run-syncdb`
3. runs `python manage.py bootstrap_school_roles`
4. verifies the auth user table
5. starts the server

## When moving to a newly extracted upgrade folder

Run:

```bat
carry_forward_old_db_windows.bat
```

Paste the OLD project folder path that contains your existing `db.sqlite3`.

The script copies:

- old `db.sqlite3`
- old `.env`, if available

Then it migrates the carried database.

## Important rule

Never copy the new ZIP over your old database without a backup. The provided scripts create backups automatically.

## Files that must not go to GitHub

- `db.sqlite3`
- `.env`
- `venv/`
- `db_backups/`
