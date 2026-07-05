# Phase 1.5 — Student & Parent Auto Account Maker

## Added

- Student login profile model: `StudentUserProfile`
- Parent login profile model: `ParentProfile`
- Parent dashboard: `/parent/dashboard/`
- Account maker dashboard: `/accounts/maker/`
- One-click student ID creation/reset
- One-click parent ID creation/reset
- Principal + Accountant + School Admin access for account maker

## Username format

- Student: `stu00001`, `stu00002`, ...
- Parent: `par00001`, `par00002`, ...

## Password behavior

A strong temporary password is generated each time an account is created or reset.
It is displayed only once on the result page.

## Required commands

```powershell
python manage.py migrate --run-syncdb
python manage.py bootstrap_school_roles
python manage.py runserver
```

The Windows BAT files already run force migration and bootstrap before server start.
