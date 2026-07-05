# Phase 1.4 — Staff Role Dropdown + Always-On Force Migration

## Applied changes

1. `AddStaffForm` now shows only approved staff roles in the Role dropdown:
   - Teacher
   - Head of Department
   - Principal
   - Accountant

2. These role rows are now seeded into the database before use:
   - Added data migration: `school/migrations/0031_seed_staff_roles.py`
   - Updated bootstrap command: `python manage.py bootstrap_school_roles`

3. Employment statuses are also seeded:
   - Permanent
   - Contract
   - Part Time
   - Probation

4. Subject is now optional for staff because Principal, HOD and Accountant may not have a subject.

5. Windows BAT scripts now run migrations and bootstrap by default before starting the server:
   - `setup_windows.bat`
   - `force_fix_auth_user_windows.bat`
   - `fix_no_auth_user_table_windows.bat`
   - `reset_local_database_windows.bat`
   - `start_server_windows.bat`

## Recommended daily run command on Windows

Double-click:

```text
start_server_windows.bat
```

This will run:

```text
python manage.py migrate --run-syncdb
python manage.py bootstrap_school_roles
python manage.py runserver
```

## Manual commands

```powershell
python manage.py migrate --run-syncdb
python manage.py bootstrap_school_roles
python manage.py runserver
```

## Verification

Open Add Staff page and check Role dropdown. It should show:

```text
Accountant
Head of Department
Principal
Teacher
```

The order is alphabetical because the form sorts by role name.
