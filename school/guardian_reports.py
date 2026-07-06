from collections import defaultdict

from django.shortcuts import render

from .access_control import admin_required
from .models import Student


@admin_required
def multi_child_guardians(request):
    students = Student.objects.select_related('grade', 'guardian_relation').filter(status=True).order_by('guardian_name', 'phone', 'name')
    grouped = defaultdict(list)
    for student in students:
        guardian = (student.guardian_name or '').strip()
        phone = (student.phone or '').strip()
        if not guardian:
            continue
        grouped[(guardian.lower(), phone)].append(student)

    records = []
    for (guardian_key, phone), children in grouped.items():
        if len(children) > 1:
            first = children[0]
            records.append({
                'guardian_name': first.guardian_name,
                'phone': phone or '-',
                'child_count': len(children),
                'children': children,
            })
    records.sort(key=lambda item: (-item['child_count'], item['guardian_name'].lower()))
    return render(request, 'multi_child_guardians.html', {
        'records': records,
        'total_records': len(records),
    })
