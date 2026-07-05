@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo Check Django Database / auth_user / staff roles
echo ============================================================
echo Current folder: %CD%
echo.

if not exist manage.py (
    echo ERROR: manage.py not found here.
    pause
    exit /b 1
)

if exist venv\Scripts\activate.bat call venv\Scripts\activate.bat

python manage.py shell -c "from django.conf import settings; from django.contrib.auth.models import User; from school.models import Role, StudentUserProfile, ParentProfile; print('DATABASE=', settings.DATABASES['default']); print('Users=', User.objects.count()); print('Staff roles=', list(Role.objects.filter(name__in=['Teacher','Head of Department','Principal','Accountant']).values_list('name', flat=True))); print('Student login profiles=', StudentUserProfile.objects.count()); print('Parent login profiles=', ParentProfile.objects.count())"
python manage.py showmigrations auth
python manage.py showmigrations school
pause
