# Admin Profile Settings MVP

This module prepares the project for dynamic admin profiles and future multi-school SaaS branding.

## URL

```text
/admin-profile/
```

## Features

- School branding profile
- Main logo upload
- Watermark logo upload
- Tenant-ready school colors
- Admin/self profile photo upload
- Browser camera capture for profile photo
- Password change
- Staff login account creation
- Role profile rules

## New models

```text
SchoolBrandProfile
UserProfileSetting
StaffLoginProfile
RoleProfileRule
```

## Migration

```text
school/migrations/0050_admin_profile_settings.py
```

## SaaS direction

For multi-school handling, the active school/tenant can later be resolved by domain, subdomain, campus code or logged-in user. Once that exists, templates should use the active `SchoolBrandProfile` or a future `SchoolTenant` record for logo, watermark, colors, address and phone.

## Camera note

The camera feature uses browser `navigator.mediaDevices.getUserMedia`. It works when the browser grants camera permission. It stores the captured frame as the current user's profile photo.
