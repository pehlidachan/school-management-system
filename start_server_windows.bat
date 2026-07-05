@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"


echo ============================================================
echo Start Server - SMART FAST MODE + force migration/bootstrap ON
echo ============================================================
echo Current folder: %CD%
echo.

if not exist manage.py (
    echo ERROR: manage.py not found in this folder.
    pause
    exit /b 1
)

if not exist venv\Scripts\python.exe (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 pause & exit /b 1
)
call venv\Scripts\activate.bat

if not exist .env copy .env.example .env >nul

REM Install requirements only when the marker is missing. Re-installing on every start is slow.
if not exist .requirements_installed (
    echo Installing requirements first time for this folder...
    python -m pip install -r requirements.txt
    if errorlevel 1 pause & exit /b 1
    echo installed>%CD%\.requirements_installed
) else (
    echo Requirements already installed. Skipping pip install for faster startup.
)

if exist db.sqlite3 (
    if not exist db_backups mkdir db_backups
    for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TS=%%i
    copy db.sqlite3 "db_backups\before_migration_!TS!.sqlite3" >nul
    echo DB backup made: db_backups\before_migration_!TS!.sqlite3
) else (
    echo No db.sqlite3 found. Django will create a fresh local database during migration.
)

echo FORCE MIGRATION ON ^(quiet mode for speed^) ...
python manage.py migrate --run-syncdb --verbosity 0
if errorlevel 1 pause & exit /b 1

echo FORCE BOOTSTRAP ON...
python manage.py bootstrap_school_roles
if errorlevel 1 pause & exit /b 1

echo Verifying database...
python manage.py shell -c "from django.contrib.auth.models import User; print('auth_user OK; users=', User.objects.count())"
if errorlevel 1 pause & exit /b 1

echo.
echo Server starting. Use these URLs:
echo Login:     http://127.0.0.1:8000/login/
echo Dashboard: http://127.0.0.1:8000/dashboard/
echo Admin:     http://127.0.0.1:8000/portal/
echo.
python manage.py runserver
pause
