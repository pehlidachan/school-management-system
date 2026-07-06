import csv
from collections import defaultdict

from django.http import HttpResponse

from .access_control import admin_required, staff_required
from .gatepass_models import GatePass
from .models import Student
from .non_teaching_models import NonTeachingStaff
from .public_models import JobApplication, OnlineAdmissionApplication, ParentComplaint


def _csv_response(filename, headers, rows):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    return response


@admin_required
def multi_child_guardians_csv(request):
    students = Student.objects.select_related('grade', 'guardian_relation').filter(status=True).order_by('guardian_name', 'phone', 'name')
    grouped = defaultdict(list)
    for student in students:
        guardian = (student.guardian_name or '').strip()
        phone = (student.phone or '').strip()
        if guardian:
            grouped[(guardian.lower(), phone)].append(student)
    rows = []
    for (guardian_key, phone), children in grouped.items():
        if len(children) > 1:
            first = children[0]
            rows.append([
                first.guardian_name,
                phone,
                len(children),
                ' | '.join(child.name for child in children),
                ' | '.join(str(child.grade or '') for child in children),
                ' | '.join(str(child.id) for child in children),
            ])
    return _csv_response('multi_child_parents.csv', ['Guardian Name', 'Phone', 'Children Count', 'Children Names', 'Classes', 'Student IDs'], rows)


@staff_required
def gatepass_csv(request):
    rows = []
    for item in GatePass.objects.select_related('student', 'staff', 'issued_by').all()[:1000]:
        rows.append([
            item.gate_pass_no,
            item.display_name,
            item.person_type,
            item.phone,
            item.destination,
            item.reason,
            item.luggage_detail,
            item.status,
            item.created_at.strftime('%Y-%m-%d %H:%M'),
        ])
    return _csv_response('gatepass_records.csv', ['Gate Pass No', 'Name', 'Type', 'Phone', 'Destination', 'Reason', 'Luggage', 'Status', 'Created At'], rows)


@admin_required
def non_teaching_staff_csv(request):
    rows = []
    for item in NonTeachingStaff.objects.select_related('employment_status').all()[:1000]:
        rows.append([
            item.id,
            item.name,
            item.appointment,
            item.department,
            item.phone,
            item.email,
            item.salary,
            item.employment_status.name if item.employment_status else '',
            'Active' if item.status else 'Inactive',
        ])
    return _csv_response('non_teaching_staff.csv', ['ID', 'Name', 'Appointment', 'Department', 'Phone', 'Email', 'Salary', 'Employment', 'Status'], rows)


@admin_required
def parent_complaints_csv(request):
    rows = [[x.id, x.parent_name, x.student_name, x.student_class, x.phone, x.email, x.subject, x.status, x.created_at.strftime('%Y-%m-%d %H:%M')] for x in ParentComplaint.objects.all()[:1000]]
    return _csv_response('parent_complaints.csv', ['ID', 'Parent', 'Student', 'Class', 'Phone', 'Email', 'Subject', 'Status', 'Created At'], rows)


@admin_required
def online_admissions_csv(request):
    rows = [[x.id, x.student_name, x.desired_class, x.father_name, x.guardian_phone, x.guardian_email, x.previous_school, x.status, x.created_at.strftime('%Y-%m-%d %H:%M')] for x in OnlineAdmissionApplication.objects.all()[:1000]]
    return _csv_response('online_admissions.csv', ['ID', 'Student', 'Desired Class', 'Father', 'Phone', 'Email', 'Previous School', 'Status', 'Created At'], rows)


@admin_required
def job_applications_csv(request):
    rows = [[x.id, x.applicant_name, x.applied_for, x.qualification, x.experience, x.phone, x.email, x.status, x.created_at.strftime('%Y-%m-%d %H:%M')] for x in JobApplication.objects.all()[:1000]]
    return _csv_response('job_applications.csv', ['ID', 'Applicant', 'Applied For', 'Qualification', 'Experience', 'Phone', 'Email', 'Status', 'Created At'], rows)
