# Phase 2.1 Attendance MVP

This phase adds the first practical school ERP module after the UI shell: class-wise daily attendance.

## Added database tables

- `AttendanceSession`
  - One attendance register for one grade/class on one date.
  - Unique per `grade + attendance_date`.
  - Tracks `taken_by`, note, created/updated timestamps.

- `StudentAttendance`
  - One row per student inside an attendance session.
  - Status values: `present`, `absent`, `late`, `leave`.
  - Tracks remarks and marked_by user.

## Added pages

- `/attendance/`
  - Attendance dashboard.
  - Select grade/class and date.
  - Shows today summary and recent sessions.

- `/attendance/mark/<grade_id>/`
  - Daily attendance register.
  - Mark each student as Present, Absent, Late, or Leave.
  - Optional remarks per student.

- `/attendance/report/`
  - Recent attendance sessions and totals.

- `/attendance/session/<session_id>/`
  - Detailed attendance records for one class/date.

## Access

Attendance pages currently use `staff_required`, so the following users can access:

- Superuser
- Django staff user
- School Admin
- Principal
- Head of Department
- Teacher
- Accountant

Later we can narrow this down so Accountant sees reports only, while Teacher/HOD can mark attendance.

## Daily workflow

After pulling this update, run:

```powershell
git pull
.\start_server_windows.bat
```

The startup script runs migrations automatically and creates the attendance tables.
