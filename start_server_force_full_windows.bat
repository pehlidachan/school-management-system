@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"


echo ============================================================
echo FULL FORCE START - reinstall requirements + force migration
 echo ============================================================
echo Use this only when normal start has package/migration problems.
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

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 pause & exit /b 1
echo installed>%CD%\.requirements_installed

if exist db.sqlite3 (
    if not exist db_backups mkdir db_backups
    for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TS=%%i
    copy db.sqlite3 "db_backups\before_full_force_!TS!.sqlite3" >nul
)

python manage.py migrate --run-syncdb --verbosity 2
if errorlevel 1 pause & exit /b 1
python manage.py bootstrap_school_roles
if errorlevel 1 pause & exit /b 1
python manage.py shell -c "from django.contrib.auth.models import User; print('auth_user OK; users=', User.objects.count())"
if errorlevel 1 pause & exit /b 1

python manage.py runserver
pause
