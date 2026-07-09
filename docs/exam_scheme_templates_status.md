# Exam Scheme Template Status

Implemented after Batch 15.

## Current state

- Scheme 1 is stored in database.
- Scheme 1 has six default items.
- Existing exams are linked to Scheme 1 after migration.
- Superuser can create Scheme 2 in Django Admin.
- A scheme can optionally be attached to a SchoolBrandProfile for future SaaS multi-school mode.

## Key URLs

```text
/exams/
/exams/add/
/admin/school/examscheme/
```
