@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo Fix: OperationalError no such table: auth_user
echo Force migration/bootstrap is ON
echo ============================================================
echo.

if not exist manage.py (
    echo ERROR: manage.py not found here.
    pause
    exit /b 1
)

if not exist venv\Scripts\python.exe (
    echo No venv found. Creating venv first...
    python -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install -r requirements.txt

if not exist .env copy .env.example .env >nul

echo Running forced migrations...
python manage.py migrate --run-syncdb --verbosity 2
if errorlevel 1 (
    echo Migration failed. Read the error above.
    pause
    exit /b 1
)

echo Creating/updating default roles/groups...
python manage.py bootstrap_school_roles
if errorlevel 1 (
    echo Bootstrap failed.
    pause
    exit /b 1
)

echo Verifying auth_user table...
python manage.py shell -c "from django.contrib.auth.models import User; print('auth_user OK; users=', User.objects.count())"
if errorlevel 1 (
    echo Verification failed.
    pause
    exit /b 1
)

echo Starting server...
python manage.py runserver
pause
