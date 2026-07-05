@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo ============================================================
echo Start Server - DB backup + force migration/bootstrap first
 echo ============================================================
echo Current folder: %CD%
echo.

if not exist manage.py (
    echo ERROR: manage.py not found in this folder.
    pause
    exit /b 1
)

if not exist venv\Scripts\python.exe python -m venv venv
call venv\Scripts\activate.bat
if not exist .env copy .env.example .env >nul

if exist db.sqlite3 (
    if not exist db_backups mkdir db_backups
    for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TS=%%i
    copy db.sqlite3 "db_backups\before_migration_!TS!.sqlite3" >nul
    echo DB backup made: db_backups\before_migration_!TS!.sqlite3
) else (
    echo No db.sqlite3 found. Django will create a fresh local database during migration.
)

python -m pip install -r requirements.txt
if errorlevel 1 pause & exit /b 1

echo FORCE MIGRATION ON...
python manage.py migrate --run-syncdb
if errorlevel 1 pause & exit /b 1

echo FORCE BOOTSTRAP ON...
python manage.py bootstrap_school_roles
if errorlevel 1 pause & exit /b 1

echo Verifying database...
python manage.py shell -c "from django.contrib.auth.models import User; print('auth_user OK; users=', User.objects.count())"
if errorlevel 1 pause & exit /b 1

python manage.py runserver
pause
