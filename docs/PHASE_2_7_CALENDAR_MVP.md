# Phase 2.7 Calendar MVP

This phase adds a SchoolHub-style school calendar module.

## Added database table

- `SchoolCalendarEvent`
  - Title and description.
  - Event type: Event, Holiday, Exam, Meeting, Deadline.
  - Audience: All, Students, Parents, Teachers, Staff.
  - Event date and optional end date.
  - Optional start/end time.
  - Location.
  - Active/inactive status.
  - Created by user.

## Added pages

- `/calendar/`
  - Calendar dashboard with today, upcoming and recent past events.

- `/calendar/add/`
  - Add new calendar event.

- `/calendar/<event_id>/`
  - Calendar event detail page.

## Access

Currently calendar pages use `staff_required`, so staff-side users can manage events:

- Superuser
- Django staff
- School Admin
- Principal
- Head of Department
- Teacher
- Accountant

Later we can make filtered read-only calendar feeds for Student and Parent dashboards.

## Sidebar

The Calendar sidebar item now opens the real school calendar instead of a placeholder.

## Future upgrades

- Monthly grid calendar view.
- Drag/drop event updates.
- Student/Parent filtered calendar.
- Exam schedule integration.
- Notice-to-calendar conversion.
- Reminders / WhatsApp notifications.
