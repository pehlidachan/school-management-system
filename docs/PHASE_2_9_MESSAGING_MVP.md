# Phase 2.9 Messaging MVP

This phase adds the first internal messaging module.

## Added database tables

- `MessageThread`
  - Subject.
  - Sender and recipient users.
  - Priority: Normal, Important, Urgent.
  - Read/unread status.
  - Last activity timestamp.

- `ThreadMessage`
  - Individual messages inside a thread.
  - Author and body.
  - Created timestamp.

## Added pages

- `/messages/`
  - Message inbox / communication center.
  - Total, unread and sent counters.

- `/messages/compose/`
  - Compose a new message to another active user.

- `/messages/<thread_id>/`
  - Thread detail and conversation history.

- `/messages/<thread_id>/reply/`
  - Reply to an existing thread.

## Access

Currently messages use `staff_required`, so staff-side users can use the messaging module.

## Sidebar

The Message sidebar item now opens the real message inbox instead of a placeholder.

## Future upgrades

- Student/Parent messaging.
- Class-wide or group messaging.
- Attachments.
- Search/filter.
- Archive/delete.
- Real-time notifications.
- WhatsApp/email bridge.
