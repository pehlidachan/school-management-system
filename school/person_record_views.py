from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .access_control import admin_required, is_school_admin
from .forms.add_staff_form import AddStaffForm
from .forms.add_student_form import AddStudentForm
from .media_utils import save_person_file
from .models import Staff, Student


def _upload(request):
    return request.FILES.get('person_image') or request.FILES.get('photo_capture') or request.FILES.get('image')


def _save_photo_path(area, record, uploaded_file):
    photo_path = save_person_file(area, record.id, uploaded_file)
    if photo_path:
        record.photo_path = photo_path
        record.save(update_fields=['photo_path'])
    return photo_path


@admin_required
def add_student(request):
    if not is_school_admin(request.user):
        messages.warning(request, 'This page is for admin only!')
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'add_student.html', {'form': AddStudentForm()})
    form = AddStudentForm(request.POST)
    if form.is_valid():
        record = form.save()
        _save_photo_path('students', record, _upload(request))
        messages.success(request, 'The student has been added successfully!')
        return redirect('display_students')
    messages.error(request, 'Please enter the valid Information!')
    return redirect('add_student')


@admin_required
def edit_student(request, id):
    if not is_school_admin(request.user):
        messages.warning(request, 'This page is for admin only!')
        return redirect('home')
    record = get_object_or_404(Student, pk=id)
    if request.method == 'GET':
        return render(request, 'edit_student.html', {'form': AddStudentForm(instance=record), 'id': id})
    form = AddStudentForm(request.POST, instance=record)
    if form.is_valid():
        record = form.save()
        _save_photo_path('students', record, _upload(request))
        messages.success(request, 'Student updated successfully!')
        return redirect('display_students')
    messages.error(request, 'please enter valid information!')
    return redirect('edit_student', id=id)


@admin_required
def add_staff(request):
    if not is_school_admin(request.user):
        messages.warning(request, 'This page is for admin only!')
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'add_staff.html', {'form': AddStaffForm()})
    form = AddStaffForm(request.POST)
    if form.is_valid():
        record = form.save()
        _save_photo_path('staff', record, _upload(request))
        messages.success(request, 'New staff added successfully!')
        return redirect('display_staff')
    messages.error(request, 'Please enter valid information!')
    return redirect('add_staff')


@admin_required
def edit_staff(request, id):
    if not is_school_admin(request.user):
        messages.warning(request, 'This page is for admin only!')
        return redirect('home')
    record = get_object_or_404(Staff, pk=id)
    if request.method == 'GET':
        return render(request, 'edit_staff.html', {'form': AddStaffForm(instance=record), 'id': id})
    form = AddStaffForm(request.POST, instance=record)
    if form.is_valid():
        record = form.save()
        _save_photo_path('staff', record, _upload(request))
        messages.success(request, 'Staff updated successfully!')
        return redirect('display_staff')
    messages.error(request, 'Please enter the valid information!')
    return redirect('edit_staff', id=id)
