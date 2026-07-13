# Admin Profile Upload Save Fix

## Problem

Users could upload or capture a profile image in the Admin Profile module, but the save action was not clear and the saved image could appear unchanged on the page.

## Fix

- Added a visible sticky `Save Profile & Picture` action near the profile picture controls.
- Added a second full-width save button at the bottom of the profile form.
- Added instant image preview when a file is selected.
- Added camera capture status text before saving.
- Added clearer success messages for profile details, profile photo, brand logo and watermark logo.
- Added optional profile photo removal checkbox.
- Added development serving for `/person_files/` so uploaded profile/logo images render locally.

## Affected page

```text
/admin-profile/
```

## Database

No migration is required. This is a view/template/static-development serving fix only.
