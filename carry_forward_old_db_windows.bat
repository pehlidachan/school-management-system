@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo ============================================================
echo Carry Forward Old db.sqlite3 Into This Upgrade Folder
echo ============================================================
echo This script copies your OLD project's db.sqlite3 into this new folder,
echo then runs force migrations and role bootstrap on the carried database.
echo.

if not exist manage.py (
    echo ERROR: manage.py not found in this folder.
    pause
    exit /b 1
)

set /p OLD_PATH=Paste OLD project folder path containing old db.sqlite3: 
set OLD_PATH=%OLD_PATH:"=%

if not exist "%OLD_PATH%\db.sqlite3" (
    echo ERROR: Could not find: "%OLD_PATH%\db.sqlite3"
    echo Open the old working folder that contains manage.py and db.sqlite3, copy its address, and try again.
    pause
    exit /b 1
)

if not exist db_backups mkdir db_backups
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TS=%%i

if exist db.sqlite3 (
    echo Current folder already has db.sqlite3. Backing it up first...
    copy db.sqlite3 "db_backups\current_before_carry_!TS!.sqlite3" >nul
)

copy "%OLD_PATH%\db.sqlite3" db.sqlite3 >nul
if errorlevel 1 (
    echo ERROR: Could not copy old db.sqlite3.
    pause
    exit /b 1
)

echo Old database copied successfully.

if exist "%OLD_PATH%\.env" (
    if exist .env (
        copy .env "db_backups\env_before_carry_!TS!.env" >nul
    )
    copy "%OLD_PATH%\.env" .env >nul
    echo Old .env copied too.
) else (
    if not exist .env copy .env.example .env >nul
)

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

if not exist .requirements_installed (
    echo Installing requirements first time for this folder...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Requirements installation failed.
        pause
        exit /b 1
    )
    echo installed>%CD%\.requirements_installed
) else (
    echo Requirements already installed. Skipping pip install for faster startup.
)

echo.
echo FORCE MIGRATION ON carried database...
python manage.py migrate --run-syncdb --verbosity 0
if errorlevel 1 (
    echo ERROR: Migration failed.
    pause
    exit /b 1
)

echo.
echo FORCE BOOTSTRAP ON roles/groups/accounts foundation...
python manage.py bootstrap_school_roles
if errorlevel 1 (
    echo ERROR: Bootstrap failed.
    pause
    exit /b 1
)

echo.
echo Verifying carried database...
python manage.py shell -c "from django.contrib.auth.models import User; from school.models import Student, Staff, Role; print('Users=', User.objects.count()); print('Students=', Student.objects.count()); print('Staff=', Staff.objects.count()); print('Staff roles=', list(Role.objects.filter(name__in=['Teacher','Head of Department','Principal','Accountant']).values_list('name', flat=True)))"
if errorlevel 1 (
    echo ERROR: Verification failed.
    pause
    exit /b 1
)

echo.
echo DONE: Old database is now carried forward into this upgraded app.
echo Starting server...
echo Open: http://127.0.0.1:8000/login/
echo.
python manage.py runserver
pause
