# CodeRabbit Safety Notes

Batch 2.1 applied the still-valid CodeRabbit safety review findings from PR #1.

## Fixed

- Removed client-writable `photo_path` from Student and Staff forms.
- Kept `photo_path` server-managed through `_save_photo_path(...)` only.
- Made `welcome_card_sent_at` server-managed in `Student.save()`.
- Excluded `welcome_card_sent_at` from the student form.
- Added safe default handling for blank `monthly_fee` form input.
- Added non-negative validation for `Student.monthly_fee`.
- Added migration `0046_student_monthly_fee_validator.py` for the validator state.
- Added model-level duplicate validation for student `gr_no` and `admission_no`.
- Added model-level duplicate validation for staff `staff_code` and `cnic`.
- Marked `photo_path` and `welcome_card_sent_at` as read-only in Django admin where applicable.

## Notes

Database-level unique constraints were intentionally not added yet because old carried-forward SQLite databases can already contain duplicate or blank values. The safer MVP approach is form/model validation first, then later run a duplicate cleanup report before adding hard DB constraints.
