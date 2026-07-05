# Phase 1.2 - Database Setup Fix

## Problem fixed

If you extract a clean project ZIP and try to log in before running migrations, Django raises:

```text
OperationalError at /login/
no such table: auth_user
```

This is not a login-code bug. It means the local database has not been initialized yet.

The clean project intentionally does not include `db.sqlite3` because the original database contained private user/student/staff records.

## Correct fix

Run migrations before login:

```powershell
python manage.py migrate
python manage.py bootstrap_school_roles
python manage.py createsuperuser
python manage.py runserver
```

## New helper scripts

This package includes three Windows helper scripts:

- `setup_windows.bat` - full setup from scratch
- `fix_no_auth_user_table_windows.bat` - quick fix for missing `auth_user` table
- `reset_local_database_windows.bat` - deletes local SQLite database and recreates it

## Recommended Windows flow

Double-click:

```text
setup_windows.bat
```

or run from terminal:

```powershell
.\setup_windows.bat
```

## Important

Every newly extracted ZIP has a new empty local environment. If `db.sqlite3` is missing, old superuser credentials from a previous folder will not work. You must create a new superuser in the new extracted folder, or copy/migrate the database intentionally.
