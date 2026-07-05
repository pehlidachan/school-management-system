@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo ============================================================
echo Backup Local SQLite Database
 echo ============================================================

if not exist manage.py (
    echo ERROR: manage.py not found in this folder.
    pause
    exit /b 1
)

if not exist db.sqlite3 (
    echo No db.sqlite3 found in this folder. Nothing to backup.
    pause
    exit /b 0
)

if not exist db_backups mkdir db_backups
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TS=%%i
copy db.sqlite3 "db_backups\db_!TS!.sqlite3" >nul
if errorlevel 1 (
    echo ERROR: backup failed.
    pause
    exit /b 1
)

echo Backup created: db_backups\db_!TS!.sqlite3
pause
