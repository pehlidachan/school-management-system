from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# models
from .models import Student, Staff, Grade, Gender, Role, Subject, EmploymentStatus, ClassAndTiming, GuardianRelation, ClassIncharge, StudentUserProfile, ParentProfile

# forms
from .forms.user_creation_form import SignupForm
from .forms.add_student_form import AddStudentForm
from .forms.add_staff_form import AddStaffForm
from .forms.add_grade_form import AddGradeForm
from .forms.add_class_and_timing import AddClassAndTimingForm
from .forms.add_gender_form import AddGenderForm
from .forms.add_class_incharge import AddClassInchargeForm
from .forms.add_guardian_relation_form import AddGuardianRelationForm
from .forms.add_role import AddRoleForm
from .forms.add_subject_form import AddSubjectForm


from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.utils.crypto import get_random_string

from .access_control import admin_required, staff_required, student_required, parent_required, account_creator_required, is_school_admin, is_school_staff, is_school_student, is_school_parent, is_account_creator, is_teacher_like


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def faqs(request):
    return render(request, 'faqs.html')

def contact(request):
    return render(request, 'contact.html')

def locations(request):
    return render(request, 'locations.html')

def signup(request):
    if request.method == 'GET':
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})
    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, 'Account request submitted. A school admin must approve it before login.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid entries! Please try again.')
            return redirect('signup')

def user_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'login.html')
    else:
        if not request.user.is_authenticated:
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username and password:
                user = authenticate(request, username=username, password=password)
                if user is None:
                    messages.error(request, 'Invalid credentials, or your account is waiting for admin approval.')
                    return redirect('login')
                else:
                    login(request, user)
                    messages.success(request, 'User logged in successfully!')
                    return redirect('dashboard')
            else:
                messages.error(request, 'Please enter both username and password!')
                return redirect('login')
        else:
            messages.warning(request, 'You have already logged in!')
            return redirect('dashboard')


@login_required(login_url='login')
def dashboard(request):
    """Send each signed-in user to the correct working area."""
    if is_school_admin(request.user):
        return redirect('portal')
    if is_account_creator(request.user):
        return redirect('account_creator_dashboard')
    if is_school_parent(request.user):
        return redirect('parent_dashboard')
    if is_school_student(request.user):
        return redirect('student_dashboard')
    if is_teacher_like(request.user):
        return redirect('teacher_dashboard')
    messages.warning(request, 'Your login exists, but no school role/profile is attached yet. Ask admin/principal to assign the correct group.')
    return redirect('home')

def user_logout(request):
    if request.user.is_authenticated:
        messages.success(request,'Logged out successfully!')
        logout(request)
    else:
        messages.error(request, 'You already have logged out!')
    return redirect('home')

'''
///////////////////////////////////////////////////////////////////////////////
                                //   Admin     //
///////////////////////////////////////////////////////////////////////////////
''' 

@admin_required
def portal(request):
    context = {
        'total_students': Student.objects.count(),
        'total_staff': Staff.objects.count(),
        'total_grades': Grade.objects.count(),
        'total_subjects': Subject.objects.count(),
        'total_classes': ClassAndTiming.objects.count(),
        'total_class_incharges': ClassIncharge.objects.count(),
        'total_roles': Role.objects.count(),
        'total_genders': Gender.objects.count(),
        'total_guardian_relations': GuardianRelation.objects.count(),
        'total_employment_statuses': EmploymentStatus.objects.count(),
        'total_student_logins': StudentUserProfile.objects.count(),
        'total_parent_logins': ParentProfile.objects.count(),
    }
    return render(request, 'portal.html', context)
'''
///////////////////////
//   Students     //
///////////////////////
''' 

@admin_required
def display_students(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            data = Student.objects.all()
            return render(request, 'display_students.html', {'data': data})
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')
        
@admin_required
def student_details(request,id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            student = get_object_or_404(Student, pk=id)
            return render(request, 'student_details.html', {'student': student})
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')
    
@admin_required
def add_student(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            if request.method == 'GET':
                form = AddStudentForm()
                return render(request, 'add_student.html', {'form': form})
            else:
                form = AddStudentForm(request.POST)
                if form.is_valid():
                    form.save()


                    
                    messages.success(request,'The student has been added successfully!')
                    return redirect('display_students')
                else:
                    messages.error(request, 'Please enter the valid Information!')
                    return redirect('add_student')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def edit_student(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_student = get_object_or_404(Student, pk=id)
            if request.method == 'GET':
                form = AddStudentForm(instance=current_student)
                return render(request, 'edit_student.html',{'form': form, 'id':id})
            else:
                form = AddStudentForm(request.POST, instance=current_student)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Student updated successfully!')
                    return redirect('display_students')
                else:
                    messages.error(request, 'please enter valid information!')
                    return redirect('edit_student', id=id)
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
@require_POST
def change_student_status(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_student = get_object_or_404(Student, pk=id)
            current_student.status = not current_student.status
            current_student.save()
            messages.success(request, f'Student {id} status updated successfully')
            return redirect('display_students')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
@require_POST
def delete_student(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_student = get_object_or_404(Student, pk=id)
            current_student.delete()
            messages.success(request, f'The student {id} has been deleted successfully!')
            return redirect('display_students')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

'''
///////////////////////
//   staff     //
///////////////////////
'''

@admin_required
def display_staff(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            staff = Staff.objects.all() 
            return render(request, 'display_staff.html', {'staff': staff})
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def staff_details(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            staff = get_object_or_404(Staff, pk=id)
            return render(request, 'staff_details.html', {'staff': staff})
        else:
                messages.warning(request, 'This page is for admin only!')
                return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')
    
@admin_required
@require_POST
def change_staff_status(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_employ = get_object_or_404(Staff, pk=id)
            current_employ.status = not current_employ.status
            current_employ.save()
            messages.success(request, f'Employ {id} status updated Successfully!')
            return redirect('display_staff')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def add_staff(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            if request.method == 'GET':
                form = AddStaffForm()
                return render(request, 'add_staff.html', {'form': form})
            else:
                form = AddStaffForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'New staff added successfully!')
                    return redirect('display_staff')
                else:
                    messages.error(request, 'Please enter valid information!')
                    return redirect('add_staff')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def edit_staff(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_employ = get_object_or_404(Staff, pk=id)
            if request.method == 'GET':
                form = AddStaffForm(instance=current_employ)
                return render(request, 'edit_staff.html', {'form':form, 'id':id})
            else:
                form = AddStaffForm(request.POST, instance=current_employ)
                if form.is_valid():
                    form.save()
                    messages.success(request, f'Employ {id} has been updated successfully!')
                    return redirect('display_staff')
                else:
                    messages.error(request, 'Please enter the valid information!')
                    return redirect('edit_staff', id=id)
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
@require_POST
def delete_staff(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_employ = get_object_or_404(Staff, pk=id)
            current_employ.delete()
            messages.success(request, f'Employ {id} deleted successfully')
            return redirect('display_staff')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

'''
//////////////////////////////////////
//   classes and timing     //
//////////////////////////////////////
''' 

@admin_required
def display_classes(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            data = ClassAndTiming.objects.all()
            return render(request, 'display_classes.html', { 'data' : data })
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
@require_POST
def change_class_status(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_class = get_object_or_404(ClassAndTiming, pk=id)
            current_class.status = not current_class.status
            current_class.save()
            messages.success(request, f'Class {current_class.class_name} status changed successfully!')
            return redirect('display_classes')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')
    
@admin_required
def class_details(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            data = get_object_or_404(ClassAndTiming, id=id)
            return render(request, 'class_details.html', { 'class':data })
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def add_class(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            a_class = ClassAndTiming.objects.all().first()
            if request.method=='GET':
                form = AddClassAndTimingForm(instance=a_class)
                return render(request, 'add_class.html', { 'form' : form })
            else:
                # .first() method is used to get the first object and if there is no object it will return None.
                check_existence = ClassAndTiming.objects.filter(class_name=request.POST['class_name']).first()
                if check_existence is None:
                    form = AddClassAndTimingForm(request.POST)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'New class added successfully')
                        return redirect('display_classes')
                    else:
                        messages.error(request, 'Invalid entries please try again')
                        return redirect('add_class')
                else:
                    messages.error(request, 'Class already exists please chose another class!')
                    return redirect('add_class')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def edit_class(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_class = get_object_or_404(ClassAndTiming, id=id)
            if request.method == 'GET':
                form = AddClassAndTimingForm(instance=current_class)
                return render(request, 'edit_class.html', {'form': form, 'id':id})
            else:
                form = AddClassAndTimingForm(request.POST, instance=current_class)
                if form.is_valid():
                    form.save()
                    messages.success(request, f'Class {id} has been updated successfully!')
                    return redirect('display_classes')
                else:
                    messages.error(request, form.errors)
                    return redirect('edit_class', id=id)
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
@require_POST
def delete_class(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_class = get_object_or_404(ClassAndTiming, id=id)
            current_class.delete()
            messages.success(request, f'Grade {id} has been deleted successfully!')
            return redirect('display_classes')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

'''
////////////////////////////////////////
//   Class Incharges     //
////////////////////////////////////////
''' 

@admin_required
def display_class_incharges(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            data = ClassIncharge.objects.all()
            return render(request, 'display_class_incharges.html',{'data':data})
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def add_class_incharge(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            if request.method == 'GET':
                form = AddClassInchargeForm()
                return render(request, 'add_class_incharge.html', {'form':form})
            else:
                form = AddClassInchargeForm(request.POST)
                if form.is_valid():
                    check_existence_teacher = ClassIncharge.objects.filter(teacher=request.POST['teacher']).first()
                    check_existence_class = ClassIncharge.objects.filter(class_obj=request.POST['class_obj']).first()
                    if check_existence_teacher:
                        messages.error(request, 'The selected teacher is already holding a class.chose anothor teacher!')            
                        return redirect('add_class_incharge')
                    elif check_existence_class:
                        messages.error(request, 'An incharge is already assigned to this class please choose a different Class.')
                        return redirect('add_class_incharge')
                    else:
                        form.save()
                        messages.success(request, 'New class incharge added successfully')
                        return redirect('display_class_incharges')
                else:
                    messages.error(request, 'Invalid entries! Please enter the valid entries.')
                    return redirect('add_class_incharge')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def edit_class_incharge(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_class_incharge = ClassIncharge.objects.get(pk=id)
            if request.method == 'GET':
                form = AddClassInchargeForm(instance=current_class_incharge)
                return render(request, 'edit_class_incharge.html', {'form': form, 'id':id})
            else:
                form = AddClassInchargeForm(request.POST, instance=current_class_incharge)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Class Incharge was successfully updated.')
                    return redirect('display_class_incharges')
                else:
                    messages.error(request, 'Invalid entries! please enter the valid entries.')
                    return redirect('edit_class_incharge', id=id)
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
@require_POST
def delete_class_incharge(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_class_incharge = get_object_or_404(ClassIncharge, pk=id)
            current_class_incharge.delete()
            messages.success(request, 'The class was successfully deleted.')
            return redirect('display_class_incharges')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

'''
///////////////////////
//   grades     //
///////////////////////
''' 

@admin_required
def display_grades(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            data = Grade.objects.all()
            return render(request, 'display_grades.html', {'data': data})
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def add_grade(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            if request.method == 'GET':
                form = AddGradeForm()
                return render(request, 'add_grade.html', {'form': form})
            else:
                form = AddGradeForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'New Grade added successfully!')
                    return redirect('display_grades')
                else:
                    messages.error(request, 'Invalid entries please try again!')
                    return redirect('add_grade')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def edit_grade(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_grade = get_object_or_404(Grade, pk=id)
            if request.method == 'GET':
                form = AddGradeForm(instance=current_grade)
                return render(request, 'edit_grade.html', {'form':form,'id':id})
            else:
                form = AddGradeForm(request.POST,instance=current_grade)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Added new grade successfully!')
                    return redirect('display_grades')
                else:
                    messages.error(request, 'Invalid entry please try again!')
                    return redirect('edit_grades', id=id)
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')
        
@admin_required
@require_POST
def delete_grade(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):        
            current_grade = get_object_or_404(Grade, id=id)
            current_grade.delete()
            messages.success(request, f'Grade {id} has been deleted successfully!')
            return redirect('display_grades')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')


'''
///////////////////////
//   Genders    //
///////////////////////
''' 

@admin_required
def display_genders(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            data = Gender.objects.all()
            return render(request, 'display_genders.html', {'data': data})
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def add_gender(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            if request.method == 'GET':
                form = AddGenderForm()
                return render(request, 'add_gender.html', {'form': form})
            else:
                form = AddGenderForm(request.POST)
                check_exists = Gender.objects.filter(name=request.POST['name']).first()
                if check_exists:
                    messages.error(request, 'Gender already exists')
                    return redirect('add_gender')
                else:
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'New Gender added successfully!')
                        return redirect('display_genders')
                    else:
                        messages.error(request, 'Invalid entries please try again!')
                        return redirect('add_gender')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def edit_gender(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_gender = get_object_or_404(Gender, pk=id)
            if request.method == 'GET':
                form = AddGenderForm(instance=current_gender)
                return render(request, 'edit_gender.html', {'form':form,'id':id})
            else:
                form = AddGenderForm(request.POST,instance=current_gender)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Added new gender successfully!')
                    return redirect('display_genders')
                else:
                    messages.error(request, 'Invalid entry please try again!')
                    return redirect('edit_gender', id=id)
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
@require_POST
def delete_gender(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_gender = get_object_or_404(Gender, id=id)
            current_gender.delete()
            messages.success(request, f'Gender {id} has been deleted successfully!')
            return redirect('display_genders')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')
'''
//////////////////////////////////////
//   Guardian Relation     //
//////////////////////////////////////
''' 

@admin_required
def display_guardian_relations(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            data = GuardianRelation.objects.all()
            return render(request, 'display_guardian_relations.html', {'data': data})
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def add_guardian_relation(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            if request.method == 'GET':
                form = AddGuardianRelationForm()
                return render(request, 'add_guardian_relation.html', {'form': form})
            else:
                form = AddGuardianRelationForm(request.POST)
                check_existence = GuardianRelation.objects.filter(name=request.POST['name']).first()
                if check_existence:
                    messages.error(request, 'Guardian relation you entered already exists')
                    return redirect('add_guardian_relation')
                else:
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'New Guardian relation added successfully')
                        return redirect('display_guardian_relations')
                    else:
                        messages.error(request, 'Invalid entry! Please enter the valid entry.')
                        return redirect('add_guardian_relation')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def edit_guardian_relation(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_guardian_relation = get_object_or_404(GuardianRelation, pk=id)
            if request.method == 'GET':
                form = AddGuardianRelationForm(instance=current_guardian_relation)
                return render(request, 'edit_guardian_relation.html', {'form':form,'id':id})
            else:
                form = AddGuardianRelationForm(request.POST,instance=current_guardian_relation)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Guardian relation updated successfully!')
                    return redirect('display_guardian_relations')
                else:
                    messages.error(request, 'Invalid entry please try again!')
                    return redirect('edit_guardian_relation', id=id)
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
@require_POST
def delete_guardian_relation(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_guardian_relation = get_object_or_404(GuardianRelation, id=id)
            current_guardian_relation.delete()
            messages.success(request, 'Guardian relation deleted successfully!')
            return redirect('display_guardian_relations')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

'''
///////////////////////
//   Role     //
///////////////////////
''' 

@admin_required
def display_roles(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            data = Role.objects.all()
            return render(request, 'display_roles.html', {'data': data})
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def add_role(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            if request.method == 'GET':
                form = AddRoleForm()
                return render(request, 'add_role.html', {'form': form})
            else:
                form = AddRoleForm(request.POST)
                check_existence = Role.objects.filter(name=request.POST['name']).first()
                if check_existence:
                    messages.error(request, 'Role you entered already exists')
                    return redirect('add_role')
                else:
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'New Role added successfully')
                        return redirect('display_roles')
                    else:
                        messages.error(request, 'Invalid entry! Please enter the valid entry.')
                        return redirect('add_role')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def edit_role(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_role = get_object_or_404(Role, pk=id)
            if request.method == 'GET':
                form = AddRoleForm(instance=current_role)
                return render(request, 'edit_role.html', {'form':form,'id':id})
            else:
                form = AddRoleForm(request.POST,instance=current_role)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Role updated successfully!')
                    return redirect('display_roles')
                else:
                    messages.error(request, 'Invalid entry please try again!')
                    return redirect('edit_role', id=id)
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
@require_POST
def delete_role(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_role = get_object_or_404(Role, id=id)
            current_role.delete()
            messages.success(request, 'Role deleted successfully!')
            return redirect('display_roles')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

'''
///////////////////////
//   Subjects    //
///////////////////////
''' 

@admin_required
def display_subjects(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            data = Subject.objects.all()
            return render(request, 'display_subjects.html', {'data':data})
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def add_subject(request):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            if request.method == 'GET':
                form = AddSubjectForm()
                return render(request, 'add_subject.html', {'form': form})
            else:
                form = AddSubjectForm(request.POST)
                check_existence = Subject.objects.filter(name=request.POST['name']).first()
                if check_existence:
                    messages.error(request, 'Subject you entered already exists')
                    return redirect('add_subject')
                else:
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'New Subject added successfully')
                        return redirect('display_subjects')
                    else:
                        messages.error(request, 'Invalid entry! Please enter the valid entry.')
                        return redirect('add_subject')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
def edit_subject(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_subject = get_object_or_404(Subject, pk=id)
            if request.method == 'GET':
                form = AddSubjectForm(instance=current_subject)
                return render(request, 'edit_subject.html', {'form':form,'id':id})
            else:
                form = AddSubjectForm(request.POST,instance=current_subject)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Subject updated successfully!')
                    return redirect('display_subjects')
                else:
                    messages.error(request, 'Invalid entry please try again!')
                    return redirect('edit_subject', id=id)
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')

@admin_required
@require_POST
def delete_subject(request, id):
    if request.user.is_authenticated:
        if is_school_admin(request.user):
            current_subject = get_object_or_404(Subject, id=id)
            current_subject.delete()
            messages.success(request, 'Subject deleted successfully!')
            return redirect('display_subjects')
        else:
            messages.warning(request, 'This page is for admin only!')
            return redirect('home')
    else:
        messages.warning(request, 'please login first!')
        return redirect('login')



# -----------------------------------------------------------------------------
# Student / Parent login account maker
# -----------------------------------------------------------------------------

def _make_temp_password():
    return get_random_string(
        12,
        allowed_chars='ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789@#$%'
    )


def _group(name):
    group, _ = Group.objects.get_or_create(name=name)
    return group


@account_creator_required
def account_creator_dashboard(request):
    students = Student.objects.select_related('grade', 'gender', 'guardian_relation').order_by('id')
    rows = []
    for student in students:
        rows.append({
            'student': student,
            'student_profile': StudentUserProfile.objects.filter(student=student).select_related('user').first(),
            'parent_profile': ParentProfile.objects.filter(student=student).select_related('user').first(),
        })
    return render(request, 'account_creator_dashboard.html', {'rows': rows})


@account_creator_required
@require_POST
@transaction.atomic
def create_student_login(request, id):
    student = get_object_or_404(Student, pk=id)
    username = f"stu{student.id:05d}"
    password = _make_temp_password()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'first_name': student.name,
            'email': student.email or '',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }
    )
    user.first_name = student.name
    user.email = student.email or ''
    user.is_active = True
    user.is_staff = False
    user.is_superuser = False
    user.set_password(password)
    user.save()
    user.groups.set([_group('Student')])
    StudentUserProfile.objects.update_or_create(
        student=student,
        defaults={'user': user, 'created_by': request.user},
    )
    request.session['created_account_result'] = {
        'role': 'Student',
        'student_name': student.name,
        'guardian_name': student.guardian_name,
        'username': username,
        'password': password,
        'created': created,
    }
    messages.success(request, f"Student login ID {'created' if created else 'reset'} for {student.name}.")
    return redirect('account_created_result')


@account_creator_required
@require_POST
@transaction.atomic
def create_parent_login(request, id):
    student = get_object_or_404(Student, pk=id)
    username = f"par{student.id:05d}"
    password = _make_temp_password()
    guardian_name = student.guardian_name or f"Parent of {student.name}"
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'first_name': guardian_name,
            'email': '',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }
    )
    user.first_name = guardian_name
    user.email = ''
    user.is_active = True
    user.is_staff = False
    user.is_superuser = False
    user.set_password(password)
    user.save()
    user.groups.set([_group('Parent')])
    ParentProfile.objects.update_or_create(
        user=user,
        defaults={'student': student, 'guardian_name': guardian_name, 'created_by': request.user},
    )
    request.session['created_account_result'] = {
        'role': 'Parent',
        'student_name': student.name,
        'guardian_name': guardian_name,
        'username': username,
        'password': password,
        'created': created,
    }
    messages.success(request, f"Parent login ID {'created' if created else 'reset'} for {guardian_name}.")
    return redirect('account_created_result')


@account_creator_required
def account_created_result(request):
    result = request.session.pop('created_account_result', None)
    if not result:
        messages.warning(request, 'No newly-created credential is available. Create or reset an account first.')
        return redirect('account_creator_dashboard')
    return render(request, 'account_created_result.html', {'result': result})

'''
///////////////////////////////////////////////////////////////////////////////
                                //   Teacher     //
///////////////////////////////////////////////////////////////////////////////
''' 

@staff_required
def teacher_dashboard(request):
    if request.user.is_authenticated:
        if is_school_staff(request.user):
            current_teacher = Staff.objects.filter(email=request.user.email).first()
            if current_teacher is None:
                messages.success(request, 'Only teachers are allowed to access this page.')
                return redirect('home')
            incharge = ClassIncharge.objects.filter(teacher=current_teacher).first()
            if incharge is None:
                messages.warning(request, 'You are not the In-charge of any class.')
                return redirect('home')
            else:
                grade = Grade.objects.filter(name = incharge.class_obj.class_name).first()
                class_and_timing = ClassAndTiming.objects.filter(class_name = grade).first()
                return render(request, 'teacher_dashboard.html' ,{'teacher':current_teacher, 'class':class_and_timing})
        else:
            messages.warning(request, 'This page is for staff only.')
            return redirect('home')
    else:
        messages.warning(request, 'Please login first!')
        return redirect('login')

'''
///////////////////////////////////////////////////////////////////////////////
                                //   Student     //
///////////////////////////////////////////////////////////////////////////////
''' 

@student_required
def student_dashboard(request):
    profile = StudentUserProfile.objects.filter(user=request.user).select_related('student__grade').first()
    current_student = profile.student if profile else Student.objects.filter(email=request.user.email).first()
    if current_student is None:
        messages.warning(request, 'This student login is not linked to a student record yet.')
        return redirect('home')
    class_and_timing = ClassAndTiming.objects.filter(class_name=current_student.grade).first()
    return render(request, 'student_dashboard.html', {'current_student': current_student, 'class': class_and_timing})


@parent_required
def parent_dashboard(request):
    profile = ParentProfile.objects.filter(user=request.user).select_related('student__grade').first()
    if profile is None:
        messages.warning(request, 'This parent login is not linked to a student record yet.')
        return redirect('home')
    current_student = profile.student
    class_and_timing = ClassAndTiming.objects.filter(class_name=current_student.grade).first()
    return render(request, 'parent_dashboard.html', {'profile': profile, 'current_student': current_student, 'class': class_and_timing})
