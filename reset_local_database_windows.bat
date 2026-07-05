@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo Reset Local SQLite Database - WARNING: deletes local data
echo Force migration/bootstrap is ON after reset
echo ============================================================
echo.
set /p CONFIRM=Type RESET to continue: 
if /I not "%CONFIRM%"=="RESET" (
    echo Cancelled.
    pause
    exit /b 0
)

if not exist venv\Scripts\python.exe python -m venv venv
call venv\Scripts\activate.bat
python -m pip install -r requirements.txt

if exist db.sqlite3 del db.sqlite3
if not exist .env copy .env.example .env >nul

python manage.py migrate --run-syncdb --verbosity 2
if errorlevel 1 (
    echo Migration failed.
    pause
    exit /b 1
)
python manage.py bootstrap_school_roles
if errorlevel 1 (
    echo Bootstrap failed.
    pause
    exit /b 1
)

echo Create new superuser for the reset database.
python manage.py createsuperuser
python manage.py runserver
pause
