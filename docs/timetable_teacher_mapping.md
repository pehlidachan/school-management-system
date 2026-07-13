# TTM-CLASS-PERIOD-01 — Timetable Teacher Mapping MVP

## Purpose

This MVP adds a weekly, day-wise timetable layer for the ERP. It answers:

- Which class has which period on which day?
- Which subject is taught in that period?
- Which teacher is assigned to that period?
- What is the start/end time and room?
- Is there a teacher/class/room clash?

## New model

`WeeklyTimetableSlot`

Main fields:

- `academic_class`
- `day_of_week`
- `period_number`
- `subject`
- `teacher`
- `start_time`
- `end_time`
- `room`
- `is_break`
- `status`
- `note`
- `created_by`

## Validation / safety

The model validates:

- End time must be after start time.
- Teaching periods require subject and teacher.
- Same class cannot have overlapping active periods.
- Same teacher cannot be assigned to overlapping active periods.
- Same room cannot be assigned to overlapping active periods.
- Same class/day/period is unique.
- Same teacher/day/period is unique for active teaching periods.

## Routes

- `/timetable/` — weekly timetable dashboard
- `/timetable/add/` — assign a period
- `/timetable/slot/<slot_id>/edit/` — edit assigned period
- `/timetable/slot/<slot_id>/delete/` — delete period
- `/timetable/<class_id>/print/` — print weekly timetable

## How to use

1. Create an Academic Session.
2. Create Academic Classes such as Grade 6 - A.
3. Create Subjects and Staff.
4. Open Timetable from the sidebar.
5. Select Academic Class.
6. Assign day, period number, subject, teacher, time, and room.
7. Print the weekly timetable.

## Relationship with older ClassAndTiming

`ClassAndTiming` remains as a legacy/basic single class timing record.

`WeeklyTimetableSlot` is the new standard for ERP timetable planning because it supports:

- Day-wise schedule
- Period-wise mapping
- Teacher clash prevention
- Room clash prevention
- Printable weekly timetable

## Future upgrades

- Substitute teacher assignment
- Drag/drop timetable builder
- Auto timetable generator
- Teacher workload report
- Room utilization report
- Student/teacher mobile timetable view
