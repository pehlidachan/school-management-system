# Phase 2.6 Notice Board MVP

This phase adds a SchoolHub-style notice board module.

## Added database table

- `Notice`
  - Title and body.
  - Audience: All, Students, Parents, Teachers, Staff.
  - Priority: Normal, Important, Urgent.
  - Publish date and optional expiry date.
  - Published/unpublished status.
  - Created by user and view count.

## Added pages

- `/notices/`
  - Notice board list with featured notice panel.

- `/notices/add/`
  - Add/publish new notice.

- `/notices/<notice_id>/`
  - Notice detail page.

## Access

Currently Notice pages use `staff_required`, so staff-side users can view/add notices:

- Superuser
- Django staff
- School Admin
- Principal
- Head of Department
- Teacher
- Accountant

Later we can expose read-only notice views to Student and Parent dashboards according to `audience`.

## Sidebar

The Notice sidebar item now opens the real notice board instead of a placeholder.

## Future upgrades

- Student/Parent filtered notice feed.
- Attachments/files with notices.
- Email/WhatsApp notify button.
- Notice acknowledgement/read receipt.
- Public notice category for school website.
