# System Reply Templates

This document defines practical dynamic reply formats for parent/student requests.

## Purpose

When a parent or student sends a request from WhatsApp, app chat, SMS, or email, the ERP should respond with a consistent system-generated format.

This batch adds the first reusable reply set:

```text
Marksheet Exams List
```

## Reply channels

### 1. WhatsApp plain-text reply

Template:

```text
school/templates/replies/whatsapp/marksheet_exams_list.txt
```

Rendered by:

```python
render_whatsapp_marksheet_exams_list(student, brand=brand)
```

Output example:

```text
📅 Request On : Sun, 21-Sep-2025
💖 Marksheet Exams List 💖

Student : (4798) Natali Jones
Class : VII (A)
Parent : Allan Reid

====== Exams List ======

(86) 1st Monthly Test
(89) Mid Term Exam
(90) 2nd Monthly Test
(95) Final Term Exam
------------------------------------------------
PRODESK SMART SCHOOL (PSI)
```

### 2. WhatsApp image/SVG card reply

Template:

```text
school/templates/replies/whatsapp/marksheet_exams_list_card.svg
```

Rendered by:

```python
render_whatsapp_marksheet_exams_card_svg(student, brand=brand)
```

This SVG is designed to match the WhatsApp reference image:

- WhatsApp light doodle background
- white reply card
- student photo on top
- request date
- title with hearts
- student/class/parent
- exams list
- school footer
- reply time

Dynamic fields:

```text
student_photo_url
request_date_display
reply_title
student_id_name
class_label
parent_name
exam_svg_rows
short_school_name
reply_time_display
```

### 3. Email reply

Templates:

```text
school/templates/replies/email/marksheet_exams_list_subject.txt
school/templates/replies/email/marksheet_exams_list.txt
school/templates/replies/email/marksheet_exams_list.html
```

Rendered by:

```python
render_email_marksheet_exams_list(student, brand=brand)
```

Returns:

```python
{
    "subject": "...",
    "text": "...",
    "html": "...",
    "context": {...},
}
```

## Helper module

```text
school/reply_template_utils.py
```

Main functions:

```python
build_marksheet_exams_list_context(student, exams=None, brand=None)
render_whatsapp_marksheet_exams_list(student, exams=None, brand=None)
render_whatsapp_marksheet_exams_card_svg(student, exams=None, brand=None)
render_email_marksheet_exams_list(student, exams=None, brand=None)
```

## Data source

The exam list comes from:

```text
Exam.objects.filter(grade=student.grade, is_published=True)
```

Sorted by:

```text
sequence
start_date
id
```

## Practical future flow

A parent/student request can be handled like this:

```text
Incoming message: marksheet
Find student by WhatsApp number / parent phone / student account
Build exam list context
Send WhatsApp text OR SVG image card
If email is available, send email HTML/text reply too
```

## Next reply templates to add

1. Marksheet detail/result card reply
2. Fee voucher reply
3. Fee dues reply
4. Attendance summary reply
5. Warning/advisory reply
6. OSP certificate reply
7. Admission status reply
8. Gate pass / movement reply
