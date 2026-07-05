@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo ============================================================
echo FORCE FIX + FORCE MIGRATION + ROLE BOOTSTRAP
echo ============================================================
echo Current folder: %CD%
echo.

if not exist manage.py (
    echo ERROR: manage.py not found in this folder.
    pause
    exit /b 1
)

if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env >nul
)

REM Keep this local fix on SQLite by clearing DATABASE_URL if present.
powershell -NoProfile -ExecutionPolicy Bypass -Command "if (Test-Path .env) { (Get-Content .env) -replace '^DATABASE_URL=.*','DATABASE_URL=' | Set-Content .env }"

if not exist venv\Scripts\python.exe (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Could not create venv. Make sure Python is installed.
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat

echo Installing requirements...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Requirements installation failed.
    pause
    exit /b 1
)

echo.
echo Database being used:
python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default'])"
if errorlevel 1 (
    echo ERROR: Django settings could not load.
    pause
    exit /b 1
)

echo.
echo FORCE MIGRATION ON: migrate --run-syncdb...
python manage.py migrate --run-syncdb --verbosity 2
if errorlevel 1 (
    echo ERROR: Migration failed.
    pause
    exit /b 1
)

echo.
echo FORCE BOOTSTRAP ON: groups + staff role dropdown rows...
python manage.py bootstrap_school_roles
if errorlevel 1 (
    echo ERROR: Bootstrap failed.
    pause
    exit /b 1
)

echo.
echo Verifying auth_user and staff role rows...
python manage.py shell -c "from django.contrib.auth.models import User; from school.models import Role; required=['Teacher','Head of Department','Principal','Accountant']; existing=list(Role.objects.filter(name__in=required).values_list('name', flat=True)); missing=[r for r in required if r not in existing]; print('auth_user OK; users=', User.objects.count()); print('staff roles=', existing); raise SystemExit(1 if missing else 0)"
if errorlevel 1 (
    echo ERROR: Verification failed. Staff role rows are missing.
    pause
    exit /b 1
)

echo.
set /p CREATEUSER=Type Y to create a new superuser for this folder/database, or press Enter to skip: 
if /I "%CREATEUSER%"=="Y" (
    python manage.py createsuperuser
)

echo.
echo Starting server from this same folder...
echo Open: http://127.0.0.1:8000/login/
echo.
python manage.py runserver
pause
