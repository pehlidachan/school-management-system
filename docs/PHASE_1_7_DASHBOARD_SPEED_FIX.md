# Phase 1.7 Dashboard + Startup Speed Fix

## Fixed

1. `/dashboard/` is now a real role-aware landing page instead of a redirect-only router.
2. Home page `Open Dashboard / Control Panel` button now opens the admin panel directly for superusers and also offers role dashboard.
3. Navbar now shows a direct `Admin Panel` link for superusers.
4. `start_server_windows.bat` keeps force migration/bootstrap ON, but skips repeated `pip install -r requirements.txt` after the first successful install.
5. `start_server_force_full_windows.bat` added for full repair mode when package/migration problems happen.
6. `carry_forward_old_db_windows.bat` now uses quiet migration and skips repeated pip install after first setup.
7. `open_dashboard_windows.bat` added to open `/dashboard/` and `/portal/` quickly.

## Daily Use

Use:

```bat
start_server_windows.bat
```

Then open:

- Login: `http://127.0.0.1:8000/login/`
- Dashboard: `http://127.0.0.1:8000/dashboard/`
- Admin Panel: `http://127.0.0.1:8000/portal/`

## When Normal Start Has Problems

Use:

```bat
start_server_force_full_windows.bat
```

This re-installs packages and runs full verbose migrations.
