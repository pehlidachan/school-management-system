from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faqs/', views.faqs, name='faqs'),
    path('contact/', views.contact, name='contact'),
    path('locations/', views.locations, name='locations'),
    # authentication
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Administrator-------------------------------------------------------------------------------------------
    path('portal/', views.portal, name='portal'),

    # Student
    # ----------------------------------------------------------------
    path('students/display/', views.display_students, name='display_students'),
    path('student/details/<int:id>/', views.student_details, name='student_details'),
    path('student/add/', views.add_student, name='add_student'),
    path('student/edit/<int:id>/', views.edit_student, name='edit_student'),
    path('student/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('student/status/change/<int:id>/', views.change_student_status, name='change_student_status'),
    # Staff
    # ----------------------------------------------------------------
    path('staff/display/', views.display_staff, name='display_staff'),
    path('staff/details/<int:id>/', views.staff_details, name='staff_details'),
    path('staff/status/change/<int:id>/', views.change_staff_status, name='change_staff_status'),
    path('staff/add/', views.add_staff, name='add_staff'),
    path('staff/edit/<int:id>/', views.edit_staff, name='edit_staff'),
    path('staff/delete/<int:id>/', views.delete_staff, name='delete_staff'),

    # Grades
    # -----------------------------------------------------------------  
    
    path('grades/display/', views.display_grades, name='display_grades'),
    path('grades/add/', views.add_grade, name='add_grade'),
    path('grades/edit/<int:id>/', views.edit_grade, name='edit_grade'),
    path('grades/delete/<int:id>/', views.delete_grade, name='delete_grade'),


    # Classes and Timings
    # ----------------------------------------------------------------

    path('classes/display/', views.display_classes, name='display_classes'),
    path('classes/details/<int:id>/', views.class_details, name='class_details'),
    path('class/status/change/<int:id>/', views.change_class_status, name= 'change_class_status'),
    path('classes/add/', views.add_class, name='add_class'),
    path('class/edit/<int:id>/', views.edit_class, name='edit_class'),
    path('class/delete/<int:id>/', views.delete_class, name='delete_class'),


    # Class Incharges
    # ------------------------------------------------------------------

    path('class/incharges/', views.display_class_incharges, name='display_class_incharges'),
    path('class/incharge/add/', views.add_class_incharge, name='add_class_incharge'),
    path('class/incharge/edit/<int:id>/', views.edit_class_incharge, name='edit_class_incharge'),
    path('class/incharge/delete/<int:id>/', views.delete_class_incharge, name='delete_class_incharge'),


    # gender   
    # ----------------------------------------------------------------

    path('genders/display/', views.display_genders, name='display_genders'),
    path('genders/add/', views.add_gender, name='add_gender'),
    path('gender/edit/<int:id>/', views.edit_gender, name='edit_gender'),
    path('gender/delete/<int:id>/', views.delete_gender, name='delete_gender'),


    # guardian relation   
    # ----------------------------------------------------------------

    path('guardian/relations/display/', views.display_guardian_relations, name='display_guardian_relations'),
    path('guardian/relation/add/', views.add_guardian_relation, name='add_guardian_relation'),
    path('guardian/relation/edit/<int:id>/', views.edit_guardian_relation, name='edit_guardian_relation'),
    path('guardian/relation/delete/<int:id>/', views.delete_guardian_relation, name='delete_guardian_relation'),


    # Roles
    # ----------------------------------------------------------------

    path('roles/display/', views.display_roles, name='display_roles'),
    path('role/add/', views.add_role, name='add_role'),
    path('role/edit/<int:id>/', views.edit_role, name='edit_role'),
    path('role/delete/<int:id>/', views.delete_role, name='delete_role'),


    # Subjects
    # ----------------------------------------------------------------

    path('subjects/display/', views.display_subjects, name='display_subjects'),
    path('subject/add/', views.add_subject, name='add_subject'),
    path('subject/edit/<int:id>/', views.edit_subject, name='edit_subject'),
    path('subject/delete/<int:id>/', views.delete_subject, name='delete_subject'),


    # Account Maker-------------------------------------------------------------------------------------------
    path('accounts/maker/', views.account_creator_dashboard, name='account_creator_dashboard'),
    path('accounts/student/<int:id>/create/', views.create_student_login, name='create_student_login'),
    path('accounts/parent/<int:id>/create/', views.create_parent_login, name='create_parent_login'),
    path('accounts/created/', views.account_created_result, name='account_created_result'),

    # Teacher-------------------------------------------------------------------------------------------
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    
    # Student-------------------------------------------------------------------------------------------
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

    # Parent-------------------------------------------------------------------------------------------
    path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),
]