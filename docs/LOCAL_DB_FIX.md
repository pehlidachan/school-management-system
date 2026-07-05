# Fix for `OperationalError: no such table: auth_user`

This error means the Django auth migrations have not been applied to the **same folder/database** from which the server is running.

## Important
Run the fix in the exact folder that contains `manage.py` and where you start `python manage.py runserver`.

If the error page shows a path such as:

```text
C:\Users\...\Downloads\school-management-system-phase1-1-dashboard\school-management-system
```

then open terminal in that exact folder, not another extracted ZIP folder.

## Easiest Windows fix
Double-click:

```text
force_fix_auth_user_windows.bat
```

It will:

1. cd into the correct folder automatically
2. create/activate venv
3. install requirements
4. force local SQLite by clearing `DATABASE_URL`
5. run `python manage.py migrate --run-syncdb`
6. verify that `auth_user` exists
7. optionally create a superuser
8. start the server
