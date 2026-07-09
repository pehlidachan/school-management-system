# Exam Scheme Templates

The exam system now supports reusable scheme templates.

## Purpose

Exam schema should not be only hardcoded in code. It should be saved as a database template so a superuser can create different schemes for different schools in future SaaS mode.

## Default saved scheme

`Scheme 1` is seeded by migration as the default scheme.

### Scheme 1 items

| Order | Item key | Display name | Weight | Major |
|---:|---|---|---:|---|
| 10 | weekly_test | Weekly Test | 5% | No |
| 20 | monthly_test | Monthly Test | 10% | No |
| 30 | quarterly_test | Quarterly Test | 15% | No |
| 40 | mid_term | Mid Term Exam | 25% | Yes |
| 50 | pre_final | Pre Final Exam | 20% | Yes |
| 60 | final | Final Exam | 25% | Yes |

## New models

```text
ExamScheme
ExamSchemeItem
```

## Attach to a school

`ExamScheme.school_brand` can optionally attach a scheme to a school profile.

Future SaaS flow:

```text
SchoolBrandProfile / SchoolTenant
  -> ExamScheme
      -> ExamSchemeItem
          -> Exam records
```

## Creating Scheme 2

A superuser can create Scheme 2 from Django Admin:

```text
/admin/school/examscheme/
```

Example:

```text
Name: Scheme 2
Code: scheme-2
School Brand: New School Campus
Default: No
Active: Yes
```

Then add custom `ExamSchemeItem` rows inline:

```text
weekly_quiz
monthly_assessment
term_1_exam
term_2_exam
annual_exam
```

Each item can define:

```text
sequence
result_weight
default_total_marks
default_passing_marks
include_in_final_result
is_major_exam
```

## Using a scheme

Open:

```text
/exams/add/
```

Select:

```text
Exam Scheme -> Scheme 1 or Scheme 2
Scheme Item -> Weekly Test / Monthly Test / custom item
Class
Academic Year
Start Date
```

The resulting `Exam` record stores:

```text
scheme
scheme_item
name
exam_type / item_key
sequence
result_weight
```

## Why this matters

This allows different schools to use different exam policies without changing code.

Examples:

```text
School A: Weekly + Monthly + Final
School B: Unit Test + Term 1 + Term 2 + Annual
School C: Monthly + Quarterly + Mid Term + Pre Final + Final
```

## Migration

```text
school/migrations/0052_exam_scheme_templates.py
```

This migration creates `Scheme 1` and links existing exam records to it.
