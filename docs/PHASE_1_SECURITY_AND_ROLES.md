# Phase 1: Security and Role Foundation

This patch implements the first set of production-readiness changes from the audit report.

## What changed

### 1. Central access-control helpers

Added `school/access_control.py` with reusable guards:

- `admin_required`
- `staff_required`
- `student_required`
- `is_school_admin`
- `is_school_staff`
- `is_school_student`

This removes the need to manually repeat authentication logic in every new view.

### 2. Default role groups

Added management command:

```bash
python manage.py bootstrap_school_roles
```

It creates these Django groups:

- School Admin
- Principal
- Teacher
- Student
- Parent
- Accountant

It also attaches safe starting model permissions to those groups.

### 3. Signup approval workflow

New signup users are now created with:

```python
is_active = False
```

This means a school admin must approve/activate new accounts from Django Admin before the user can log in.

### 4. POST-only delete and status actions

Delete/status-change views now use `@require_POST`.

This prevents destructive actions from being triggered by a simple link, browser preview, crawler, or accidental GET request.

### 5. Template forms for delete/status

GET links for delete/status were replaced with POST forms and CSRF tokens.

### 6. Bug fixes included

- Staff edit now updates the existing staff record instead of accidentally creating a new one.
- Class incharge delete now fetches the existing record before deleting.
- Several `.objects.get(...)` calls were converted to `get_object_or_404(...)` for safer error handling.
- Teacher dashboard no longer redirects to itself when the teacher has no assigned class.

## Next phase

Phase 2 should add proper user-profile linking models:

- `StudentUserProfile`
- `StaffUserProfile`
- `ParentProfile`

This is needed because email matching is not strong enough for production school software.
