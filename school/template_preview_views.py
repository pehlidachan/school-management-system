from django.shortcuts import render

from .access_control import admin_required


TEMPLATE_PREVIEWS = [
    {
        "title": "Student Bio Data",
        "category": "Students",
        "icon": "fa-file-lines",
        "badge": "Profile",
        "description": "Student profile, guardian information, class details and photo area.",
        "sample": "Student name, father/guardian, class, roll no, phone, address, admission record and principal signature.",
    },
    {
        "title": "Staff Bio Data",
        "category": "Staff",
        "icon": "fa-user-tie",
        "badge": "Profile",
        "description": "Staff profile sheet with role, subject, CNIC, contact and department.",
        "sample": "Staff code, name, father/husband name, qualification, role, subject, phone, CNIC and signature area.",
    },
    {
        "title": "Student ID Card",
        "category": "Cards",
        "icon": "fa-id-badge",
        "badge": "Card",
        "description": "Compact printable ID card design for students.",
        "sample": "School header, student name, class, roll number, guardian phone, photo area and school seal.",
    },
    {
        "title": "Staff ID Card",
        "category": "Cards",
        "icon": "fa-address-card",
        "badge": "Card",
        "description": "Printable ID card for teaching and staff members.",
        "sample": "Staff name, role, subject/department, phone, staff code, photo area and authority signature.",
    },
    {
        "title": "Welcome Card",
        "category": "Students",
        "icon": "fa-gift",
        "badge": "Card",
        "description": "New admission welcome card with sent/pending workflow.",
        "sample": "Welcome message, student name, class, guardian, admission no and principal signature.",
    },
    {
        "title": "Certificates",
        "category": "Documents",
        "icon": "fa-award",
        "badge": "Print",
        "description": "Portrait Character, Hope, Provisional, Leaving and Appreciation certificates.",
        "sample": "Decorated border, school watermark, certificate heading, student details and head teacher signature.",
    },
    {
        "title": "Advisory Letters",
        "category": "Documents",
        "icon": "fa-triangle-exclamation",
        "badge": "Letter",
        "description": "Parent communication letters for conduct, attendance, office reminder and performance.",
        "sample": "Subject, student identity, parent message, follow-up instructions and signature blocks.",
    },
    {
        "title": "Fee Voucher",
        "category": "Finance",
        "icon": "fa-receipt",
        "badge": "Voucher",
        "description": "School and parent copy of fee voucher with fee heads and balance.",
        "sample": "Tuition fee, activities fee, miscellaneous fee, fine, discount, net total, paid and balance.",
    },
    {
        "title": "Dues Statement",
        "category": "Finance",
        "icon": "fa-money-bill-wave",
        "badge": "Dues",
        "description": "Student dues statement with copyable WhatsApp message.",
        "sample": "Student information, invoice rows, total outstanding dues and parent message box.",
    },
    {
        "title": "Exam Date Sheet",
        "category": "Exams",
        "icon": "fa-calendar-days",
        "badge": "Schedule",
        "description": "Class-wise printable examination date sheet.",
        "sample": "Exam name, class, date, day, subject, time, total marks, passing marks and instructions.",
    },
    {
        "title": "Result Card",
        "category": "Exams",
        "icon": "fa-square-poll-vertical",
        "badge": "Result",
        "description": "Student and bulk result card printing for exam marks.",
        "sample": "Subject-wise marks, total, obtained, percentage, pass/fail status and remarks area.",
    },
    {
        "title": "Staff Lecture Attendance Report",
        "category": "Attendance",
        "icon": "fa-clipboard-user",
        "badge": "Report",
        "description": "Staff lecture attendance report with summary and print option.",
        "sample": "Session title, date, present/absent/late/leave summary, staff rows and remarks.",
    },
    {
        "title": "Learning Resource",
        "category": "Study",
        "icon": "fa-book-open-reader",
        "badge": "Resource",
        "description": "Class and subject wise learning material detail page.",
        "sample": "Title, class, subject, description, content, link and copy share text box.",
    },
    {
        "title": "Vendor Account",
        "category": "Ledger",
        "icon": "fa-store",
        "badge": "Ledger",
        "description": "Vendor ledger with debit/credit entries and running balance.",
        "sample": "Vendor contact, date, description, debit, credit, payment method, notes and print action.",
    },
    {
        "title": "Cashbook",
        "category": "Ledger",
        "icon": "fa-cash-register",
        "badge": "Register",
        "description": "Cash and bank transaction register.",
        "sample": "Account, transaction date, title, income/expense/transfer type, amount and note.",
    },
]


@admin_required
def template_preview_center(request):
    return render(request, "template_preview_center.html", {"templates": TEMPLATE_PREVIEWS})
