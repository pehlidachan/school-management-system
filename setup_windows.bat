@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo School Management System - Windows Local Setup
echo Force migration/bootstrap is ON by default
echo ============================================================
echo.

if not exist manage.py (
    echo ERROR: manage.py not found in this folder.
    echo Put this BAT file inside the folder that contains manage.py.
    pause
    exit /b 1
)

if not exist venv\Scripts\python.exe (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment. Make sure Python is installed.
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing requirements...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Requirements installation failed.
    pause
    exit /b 1
)

if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env >nul
)

echo.
echo FORCE MIGRATION: running migrate --run-syncdb every time...
python manage.py migrate --run-syncdb --verbosity 2
if errorlevel 1 (
    echo Migration failed. Read the error above.
    pause
    exit /b 1
)

echo.
echo FORCE BOOTSTRAP: creating default groups, staff roles, employment statuses...
python manage.py bootstrap_school_roles
if errorlevel 1 (
    echo Bootstrap failed. Read the error above.
    pause
    exit /b 1
)

echo.
echo Verifying database tables and default staff roles...
python manage.py shell -c "from django.contrib.auth.models import User; from school.models import Role; print('Users=', User.objects.count()); print('Staff roles=', list(Role.objects.filter(name__in=['Teacher','Head of Department','Principal','Accountant']).values_list('name', flat=True)))"
if errorlevel 1 (
    echo ERROR: database verification failed.
    pause
    exit /b 1
)

echo.
set /p CREATEUSER=Type Y to create a new superuser, or press Enter to skip: 
if /I "%CREATEUSER%"=="Y" (
    python manage.py createsuperuser
)

echo.
echo Setup completed. Starting server...
echo Open: http://127.0.0.1:8000/login/
echo.
python manage.py runserver
pause
