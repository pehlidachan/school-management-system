# Phase 1.9 SchoolHub-style UI Shell

This phase starts converting the project from a basic Bootstrap layout into a modern SchoolHub-inspired dashboard UI.

## Added

- `static/css/dashboard.css` for the new dashboard theme.
- `school/templates/dashboard_base.html` as the reusable dashboard shell.
- `school/templates/dashboard_sidebar.html` for left navigation.
- `school/templates/dashboard_topbar.html` for search/profile/notification area.

## Redesigned pages

- `/dashboard/` role-aware landing page.
- `/portal/` admin control panel.
- `/students/display/` students list.
- `/staff/display/` teachers/staff list.
- `/accounts/maker/` student and parent ID maker.

## Design language

- Light gray app background.
- White rounded cards.
- Soft shadows.
- Blue active sidebar navigation.
- Rounded tables with light blue headers.
- Status badges for active/inactive/pending states.
- Top search/profile bar.

## Not yet functional

The sidebar now shows placeholders for future modules:

- Attendance
- Finance
- Notice
- Calendar
- Library
- Message

These links are visual placeholders for the roadmap. Backend modules will be added gradually in upcoming phases.

## Daily update workflow

After this commit, run:

```powershell
git pull
.\start_server_windows.bat
```

The browser should open the dashboard automatically after the server starts.
