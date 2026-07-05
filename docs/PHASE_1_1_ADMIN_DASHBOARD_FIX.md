# Phase 1.1 — Admin Dashboard Visibility Fix

## Problem
After a superuser logged in successfully, the app redirected to the public home page. The admin actions existed under `/portal/`, but the workflow was not obvious.

## Fixes Applied

1. Added `/dashboard/` route.
2. Login now redirects to `/dashboard/` instead of the public home page.
3. `/dashboard/` sends users to the correct panel:
   - Superuser / School Admin / Principal -> `/portal/`
   - Staff-side user -> `/teacher/dashboard/`
   - Student-side user -> `/student/dashboard/`
4. Navbar now shows a clear **Dashboard** link only after login.
5. Home page now shows **Open Dashboard / Control Panel** for logged-in users.
6. Admin portal redesigned into an actionable control panel with:
   - Add Student
   - Add Staff
   - View Students
   - View Staff
   - Classes & Timetable
   - Class Incharge
   - Grades
   - Subjects
   - Roles
   - Gender
   - Guardian Relation
   - Employment Status via Django Admin
7. Fixed Staff add/edit forms:
   - Add Staff no longer uses an undefined instance variable.
   - Edit Staff now updates the existing staff record instead of creating a new duplicate.

## How to Check

1. Start the server.
2. Login with superuser.
3. You should be redirected to `/dashboard/`, then `/portal/`.
4. You should see the Admin Control Panel with action buttons.

Direct URL:

```text
http://127.0.0.1:8000/dashboard/
```

Admin portal:

```text
http://127.0.0.1:8000/portal/
```
