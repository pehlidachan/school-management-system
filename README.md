# School Management System

Django-based school management project for students, staff, classes, subjects, roles, grades, genders, guardian relations, and class incharges.

## What's included

- Django project: `a_project`
- Main app: `school`
- Templates and static files
- Existing Django migrations
- Environment-based database configuration for SQLite or PostgreSQL/Supabase

## What's intentionally excluded

- `venv/` virtual environment
- `db.sqlite3` database file
- `__pycache__/` and compiled Python files
- `.env` secrets

The original SQLite database contained user/student/staff records, so it should not be committed publicly.


## Windows quick setup / login database fix

If you see this error:

```text
OperationalError at /login/
no such table: auth_user
```

it means migrations were not run in this newly extracted folder. Run:

```powershell
python manage.py migrate
python manage.py bootstrap_school_roles
python manage.py createsuperuser
python manage.py runserver
```

For an easier Windows setup, double-click:

```text
setup_windows.bat
```

For only the missing `auth_user` table error, double-click:

```text
fix_no_auth_user_table_windows.bat
```

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## Supabase/PostgreSQL setup

1. Create or open your Supabase project.
2. Copy the PostgreSQL connection string from Supabase.
3. Put it in `.env` as `DATABASE_URL`, for example:

```env
DATABASE_URL=postgresql://postgres:<PASSWORD>@db.<PROJECT_REF>.supabase.co:5432/postgres?sslmode=require
```

4. Run migrations:

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Next development ideas

- Add school profile settings.
- Add fee slips and fee records.
- Add attendance.
- Add DMC/result card generator.
- Add printable PDF exports.
- Improve dashboard design.
- Add role-based permissions for admin, teacher, and student dashboards.

## Phase 1 Security / Role Setup

After running migrations and creating a superuser, run:

```bash
python manage.py bootstrap_school_roles
```

This creates default Django groups for School Admin, Principal, Teacher, Student, Parent and Accountant.

New signup accounts are inactive by default. Activate approved users from Django Admin and assign the correct group before giving them access.

Delete and status-change actions are now POST-only and protected with CSRF forms.


## Upgrade / Database Carry-Forward Rule

For every new upgrade, keep your old local database. Do **not** reset unless you intentionally want fresh data.

Recommended when you extract a new upgrade ZIP:

```bat
carry_forward_old_db_windows.bat
```

Daily start:

```bat
start_server_windows.bat
```

`start_server_windows.bat` now backs up `db.sqlite3`, runs force migrations, bootstraps default roles, verifies `auth_user`, and then starts the server.

See: `docs/DATABASE_CARRY_FORWARD_STRATEGY.md`
