# Academic Class Scheme

This batch upgrades the old class system into a SaaS-ready class scheme.

## Why this was needed

Old structure:

```text
Grade = class name
ClassAndTiming = timetable
ClassIncharge = class teacher mapping
```

This was useful for MVP, but incomplete for advanced ERP/SaaS because it did not support:

```text
academic year / session
sections A/B/C
school/campus/tenant attachment
capacity
room
class teacher
admission open/closed
class-level monthly fee
class subject scheme
promotion target
```

## New structure

```text
AcademicSession
  -> AcademicClass
      -> AcademicClassSubject
      -> ClassAndTiming
      -> Students
```

## New models

### AcademicSession

Stores school year/session.

```text
name
code
school_brand
start_date
end_date
is_active
is_admission_open
note
```

Example:

```text
Session 2026
Session 2027
```

### AcademicClass

Stores a real class section for a session.

```text
school_brand
academic_session
grade
section
class_label
class_code
level_order
room
capacity
class_teacher
admission_open
monthly_fee
promotion_target
status
note
```

Example:

```text
Session 2026 -> Grade 6 -> Section A
Session 2026 -> Grade 6 -> Section B
Session 2026 -> Grade 7 -> Section A
```

### AcademicClassSubject

Stores subject scheme per class.

```text
academic_class
subject
teacher
is_core
weekly_periods
total_marks
passing_marks
sort_order
status
note
```

Example:

```text
Grade 6-A -> English -> Sir Ali -> 5 weekly periods
Grade 6-A -> Mathematics -> Sir Ahmed -> 6 weekly periods
```

## Existing model links

### Student

Student now has optional:

```text
academic_class
```

If an academic class is selected, the old `grade` is automatically aligned with the academic class grade.

### ClassAndTiming

Class timetable now has optional:

```text
academic_class
```

If an academic class is selected, old `class_name` / Grade is automatically aligned.

## Migration seed

Migration creates:

```text
Session 2026
```

Then for every old Grade, it creates Section A:

```text
Grade 6 -> Grade 6 - A
Grade 7 -> Grade 7 - A
```

It also links existing students and existing timetables to the new AcademicClass records.

## Admin URLs

```text
/admin/school/academicsession/
/admin/school/academicclass/
/admin/school/academicclasssubject/
```

## Future SaaS use

A school/campus can have its own class setup:

```text
SchoolBrandProfile
  -> AcademicSession
      -> AcademicClass
          -> AcademicClassSubject
```

This allows:

```text
School A: Grade 6-A, Grade 6-B
School B: Class 6 Red, Class 6 Blue
School C: Year 7 Alpha, Year 7 Beta
```

## Promotion use

`AcademicClass.promotion_target` can point to the next class.

Example:

```text
Grade 6-A -> Grade 7-A
Grade 7-A -> Grade 8-A
```

Later, a promotion module can use this relation to promote all selected students.

## Class fee use

`AcademicClass.monthly_fee` can become the default monthly fee for new admissions. Student-level `monthly_fee` still exists for exceptions/scholarships.
