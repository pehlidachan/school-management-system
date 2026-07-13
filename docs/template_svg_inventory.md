# Template SVG Inventory and Upload Checklist

This file is the master checklist for converting uploaded SVG designs into dynamic Django templates.

## How SVG conversion will work

For every template, the SVG should normally be used as the visual design layer. Dynamic values should be rendered by Django HTML/CSS overlay or by inline SVG template rendering.

Recommended structure:

```text
static/templates/svg/<template_key>.svg
school/templates/print/<template_key>.html
```

Dynamic data should use Django variables such as:

```django
{{ student.name }}
{{ student.gr_no }}
{{ staff.name }}
{{ invoice.net_total }}
{{ exam.name }}
{{ active_school.school_name }}
{{ active_school.main_logo.url }}
{{ active_school.watermark_logo.url }}
```

## Standard sizes

| Type | Standard size | Use |
|---|---:|---|
| A4 Portrait | 210mm x 297mm | Bio data, certificates, letters, reports |
| A4 Landscape | 297mm x 210mm | Marksheet, result card, wide certificates |
| A5 Portrait | 148mm x 210mm | Short advisory/warning letters |
| CR80 ID Card | 85.6mm x 53.98mm | Student/staff ID cards |
| Vertical PVC Card | 54mm x 86mm | Vertical staff/student cards |
| Welcome/Birthday Card | 86mm x 125mm | Welcome card, birthday card |
| WhatsApp Square | 1080px x 1080px | Share image preview |
| WhatsApp Portrait | 1080px x 1350px | Voucher/marksheet share preview |
| WhatsApp Status | 1080px x 1920px | Full screen status/share card |
| WhatsApp Reply Screenshot | 522px x 715px | App/chat reply reference style |

## Logo rule for all templates

Each SVG/template must separate logo identity:

1. Main logo: clear, sharp, 100 percent opacity.
2. Watermark logo: large background logo, 20-30 percent opacity.

Future multi-school SaaS templates should not hardcode school name, logo, address or colors. Use an active school/tenant profile.

---

## SVG upload checklist

Status legend:

- `MISSING SVG`: upload required.
- `READY TO CONNECT`: SVG uploaded and waiting for dynamic mapping.
- `DYNAMIC DONE`: connected to Django variables.
- `NOT NEEDED`: pure HTML layout is enough.

| # | Template key | User-facing template | Standard size | Expected SVG filename | Current Django template / route | Dynamic source | Status |
|---:|---|---|---|---|---|---|---|
| 1 | student_biodata | Student Bio Data | A4 Portrait | `school/templates/print/svg/student_biodata.svg` | `school/templates/print/student_biodata.html` | `Student`, active school | DYNAMIC DONE |
| 2 | staff_biodata | Staff Bio Data | A4 Portrait | `school/templates/print/svg/staff_biodata.svg` | `school/templates/print/staff_biodata.html` | `Staff`, active school | DYNAMIC DONE |
| 3 | school_leaving_certificate | School Leaving Certificate | A4 Portrait | `school_leaving_certificate.svg` | `school/templates/print/student_certificate.html` | `Student`, certificate context | MISSING SVG |
| 4 | character_certificate | Character Certificate | A4 Portrait | `character_certificate.svg` | `school/templates/print/student_certificate.html` | `Student`, certificate context | MISSING SVG |
| 5 | hope_certificate | Hope Certificate | A4 Portrait | `hope_certificate.svg` | `school/templates/print/student_certificate.html` | `Student`, certificate context | MISSING SVG |
| 6 | provisional_certificate | Provisional Certificate | A4 Portrait | `provisional_certificate.svg` | `school/templates/print/student_certificate.html` | `Student`, certificate context | MISSING SVG |
| 7 | appreciation_certificate | Appreciation Certificate | A4 Landscape | `appreciation_certificate.svg` | `school/templates/print/student_certificate.html` | `Student`, certificate context | MISSING SVG |
| 8 | experience_certificate | Staff Experience Certificate | A4 Portrait | `experience_certificate.svg` | To be added/linked | `Staff` | MISSING SVG - ROUTE/TEMPLATE ALSO NEEDED |
| 9 | appointment_letter | Staff Appointment Letter | A4 Portrait | `appointment_letter.svg` | To be added/linked | `Staff` | MISSING SVG - ROUTE/TEMPLATE ALSO NEEDED |
| 10 | student_id_card_front | Student ID Card Front | CR80 | `student_id_card_front.svg` | `school/templates/print/student_id_card.html` | `Student` | MISSING SVG |
| 11 | student_id_card_back | Student ID Card Back | CR80 | `student_id_card_back.svg` | `school/templates/print/student_id_card.html` | `Student`, active school | MISSING SVG |
| 12 | staff_id_card_front | Staff ID Card Front | CR80 | `staff_id_card_front.svg` | `school/templates/print/staff_id_card.html` | `Staff` | MISSING SVG |
| 13 | staff_id_card_back | Staff ID Card Back | CR80 | `staff_id_card_back.svg` | `school/templates/print/staff_id_card.html` | `Staff`, active school | MISSING SVG |
| 14 | student_welcome_card | Student Welcome Card | 86mm x 125mm | `student_welcome_card.svg` | `school/templates/print/student_welcome_card.html` | `Student` | MISSING SVG |
| 15 | staff_birthday_card | Staff Birthday Card | 86mm x 125mm | `staff_birthday_card.svg` | To be added/linked | `Staff` | MISSING SVG - ROUTE/TEMPLATE ALSO NEEDED |
| 16 | fee_voucher | Fee Voucher | A4 Portrait / 3 copies | `fee_voucher.svg` | `school/templates/print/fee_voucher.html` | `FeeInvoice`, `Student` | MISSING SVG |
| 17 | fee_receipt | Fee Receipt | A5 or A4 half | `fee_receipt.svg` | `school/templates/print/fee_receipt.html` | `FeeInvoice`, `Student` | MISSING SVG |
| 18 | student_dues_statement | Student Dues Statement | A4 Portrait | `student_dues_statement.svg` | `school/templates/print/student_dues_statement.html` | `Student`, invoice list | MISSING SVG |
| 19 | whatsapp_fee_voucher | WhatsApp Fee Voucher Share | 1080px x 1350px | `whatsapp_fee_voucher.svg` | To be added/linked | `FeeInvoice`, `Student` | MISSING SVG - ROUTE/TEMPLATE ALSO NEEDED |
| 20 | whatsapp_dues_message | WhatsApp Dues Message | 1080px x 1350px | `whatsapp_dues_message.svg` | Existing dues text area / future image | `Student`, invoice list | MISSING SVG - IMAGE TEMPLATE NEEDED |
| 21 | exam_datesheet | Exam Date Sheet | A4 Portrait or Landscape | `exam_datesheet.svg` | `school/templates/print/exam_datesheet.html` | `Exam`, `ExamSubject` | MISSING SVG |
| 22 | result_card | Result Card / DMC | A4 Landscape | `result_card.svg` | `school/templates/print/result_card.html` | `Exam`, `Student`, marks | MISSING SVG |
| 23 | marksheet_whatsapp_list | WhatsApp Marksheet Exams List | WhatsApp Reply Screenshot / 522px x 715px | `marksheet_whatsapp_list.svg` | `school/templates/replies/whatsapp/marksheet_exams_list_card.svg` | `Student`, published exam list, active school | DYNAMIC DONE |
| 24 | marksheet_whatsapp_detail | WhatsApp Student Exam Marksheet | 1080px x 1350px | `marksheet_whatsapp_detail.svg` | To be added/linked | `Student`, `Exam`, result image | MISSING SVG - ROUTE/TEMPLATE ALSO NEEDED |
| 25 | warning_list_whatsapp | WhatsApp Issued Warnings List | 1080px x 1350px | `warning_list_whatsapp.svg` | To be added/linked | `Student`, warning list | MISSING SVG - MODULE NEEDED |
| 26 | warning_detail_letter | Warning Detail Letter | A4 Portrait | `warning_detail_letter.svg` | Advisory letter template existing | `Student`, letter context | MISSING SVG |
| 27 | advisory_attendance | Attendance Advisory Letter | A4 Portrait | `advisory_attendance.svg` | `student_advisory_letter` | `Student`, letter context | MISSING SVG |
| 28 | advisory_conduct | Conduct Advisory Letter | A4 Portrait | `advisory_conduct.svg` | `student_advisory_letter` | `Student`, letter context | MISSING SVG |
| 29 | advisory_performance | Performance Advisory Letter | A4 Portrait | `advisory_performance.svg` | `student_advisory_letter` | `Student`, letter context | MISSING SVG |
| 30 | osp_certificate | OSP / Overall Performance Certificate | A4 Landscape | `osp_certificate.svg` | Certificates module / future OSP | `Student`, date range, metrics | MISSING SVG - ROUTE/TEMPLATE MAY NEED UPGRADE |
| 31 | class_register | Class Register | A4 Portrait | `class_register.svg` | `class_register` route | `Student`, `Grade` | MISSING SVG |
| 32 | student_attendance_report | Student Attendance Report | A4 Portrait | `student_attendance_report.svg` | attendance report pages | `AttendanceSession`, records | MISSING SVG |
| 33 | staff_lecture_attendance_report | Staff Lecture Attendance Report | A4 Portrait | `staff_lecture_attendance_report.svg` | staff attendance detail | `StaffLectureSession`, records | MISSING SVG |
| 34 | study_material_detail | Learning Resource Print | A4 Portrait | `study_material_detail.svg` | `study_material_detail.html` | `StudyMaterial` | MISSING SVG |
| 35 | vendor_account | Vendor Account / Ledger | A4 Portrait | `vendor_account.svg` | `vendor_detail.html` | `Vendor`, ledger entries | MISSING SVG |
| 36 | cashbook_report | Cashbook Report | A4 Portrait | `cashbook_report.svg` | `cashbook.html` | `CashBankTransaction` | MISSING SVG |
| 37 | school_calendar_events | School Calendar Events WhatsApp | 1080px x 1350px | `school_calendar_events.svg` | calendar module / future share image | `SchoolCalendarEvent` | MISSING SVG - IMAGE TEMPLATE NEEDED |
| 38 | notice_board | Notice Board Print/Share | A4 Portrait / 1080px | `notice_board.svg` | notice module | `Notice` | MISSING SVG |
| 39 | online_admission_application | Online Admission Application | A4 Portrait | `online_admission_application.svg` | online requests center | `OnlineAdmissionApplication` | MISSING SVG |
| 40 | job_application | Job Application / CV Print | A4 Portrait | `job_application.svg` | online requests center | `JobApplication` | MISSING SVG |
| 41 | parent_complaint | Parent Complaint Print | A4 Portrait | `parent_complaint.svg` | online requests center | `ParentComplaint` | MISSING SVG |
| 42 | gatepass | Gate Pass | A5 Portrait | `gatepass.svg` | gatepass export/list module | `GatePass` | MISSING SVG |
| 43 | library_issue_slip | Library Issue Slip | A5 Portrait | `library_issue_slip.svg` | library module | `LibraryIssue`, `LibraryBook` | MISSING SVG |
| 44 | message_thread_print | Message Thread Print | A4 Portrait | `message_thread_print.svg` | message module | `MessageThread`, replies | MISSING SVG |
| 45 | admin_profile_card | Admin/User Profile Card | 1080px or A5 | `admin_profile_card.svg` | `admin_profile_center.html` | `UserProfileSetting`, active school | MISSING SVG |
| 46 | school_brand_header | School Brand Header | SVG partial | `school_brand_header.svg` | shared header partial planned | active school | MISSING SVG - SHARED PARTIAL NEEDED |
| 47 | school_watermark_logo | School Watermark Logo | SVG partial | `school_watermark_logo.svg` | shared logo CSS/include | active school | MISSING SVG - SHARED PARTIAL NEEDED |
| 48 | dmc_grade_6 | Grade 6 DMC | A4 Landscape or Portrait | `dmc_grade_6.svg` | Not in app yet | Grade 6 marks | MISSING SVG - MODULE NEEDED IF REQUIRED |
| 49 | dmc_grade_7 | Grade 7 DMC | A4 Landscape or Portrait | `dmc_grade_7.svg` | Not in app yet | Grade 7 marks | MISSING SVG - MODULE NEEDED IF REQUIRED |

---

## Current sync count

```text
Total templates: 49
Dynamic synced templates: 3
Pending templates: 46
```

Synced templates:

1. `student_biodata`
2. `staff_biodata`
3. `marksheet_whatsapp_list`

---

## Priority conversion order

1. `school_leaving_certificate.svg`
2. `experience_certificate.svg`
3. `fee_voucher.svg`
4. `result_card.svg`
5. `student_id_card_front.svg` and `student_id_card_back.svg`
6. `staff_id_card_front.svg` and `staff_id_card_back.svg`
7. WhatsApp image templates
8. Remaining reports and slips

## What to upload for every SVG

For each SVG, upload the design file and mention the template key from the checklist.

Example:

```text
Template key: school_leaving_certificate
File: school_leaving_certificate.svg
Size: A4 Portrait
```

If the uploaded SVG does not match a checklist item, it should be added as a new row. If any expected template is missing from the upload batch, it must be highlighted before conversion continues.

## Conversion checklist for each SVG

For each template conversion, confirm:

- Correct standard size.
- One font family unless user says otherwise.
- Main logo is separate from watermark logo.
- Watermark opacity is around 20-30 percent.
- Student/staff/photo area is positioned and filled correctly.
- Dynamic text fields map to Django values.
- Browser print preview matches the uploaded SVG.
- No hardcoded school details except fallback defaults.
