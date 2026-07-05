"""
URL configuration for a_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from school import attendance_views, calendar_views, dashboard_views, exam_views, finance_views, library_views, login_views, message_views, notice_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_views.user_login, name='login'),
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('attendance/', attendance_views.attendance_dashboard, name='attendance_dashboard'),
    path('attendance/mark/<int:grade_id>/', attendance_views.mark_attendance, name='mark_attendance'),
    path('attendance/report/', attendance_views.attendance_report, name='attendance_report'),
    path('attendance/session/<int:session_id>/', attendance_views.attendance_session_detail, name='attendance_session_detail'),
    path('finance/', finance_views.finance_dashboard, name='finance_dashboard'),
    path('finance/fees/', finance_views.fees_collection, name='fees_collection'),
    path('finance/fees/add/', finance_views.add_fee_invoice, name='add_fee_invoice'),
    path('finance/fees/<int:invoice_id>/paid/', finance_views.mark_fee_paid, name='mark_fee_paid'),
    path('finance/fees/<int:invoice_id>/receipt/', finance_views.fee_receipt, name='fee_receipt'),
    path('finance/expenses/', finance_views.school_expenses, name='school_expenses'),
    path('finance/expenses/add/', finance_views.add_school_expense, name='add_school_expense'),
    path('notices/', notice_views.notice_board, name='notice_board'),
    path('notices/add/', notice_views.add_notice, name='add_notice'),
    path('notices/<int:notice_id>/', notice_views.notice_detail, name='notice_detail'),
    path('calendar/', calendar_views.calendar_dashboard, name='calendar_dashboard'),
    path('calendar/add/', calendar_views.add_calendar_event, name='add_calendar_event'),
    path('calendar/<int:event_id>/', calendar_views.calendar_event_detail, name='calendar_event_detail'),
    path('library/', library_views.library_dashboard, name='library_dashboard'),
    path('library/books/add/', library_views.add_library_book, name='add_library_book'),
    path('library/issue/', library_views.issue_library_book, name='issue_library_book'),
    path('library/issue/<int:issue_id>/return/', library_views.return_library_book, name='return_library_book'),
    path('messages/', message_views.message_inbox, name='message_inbox'),
    path('messages/compose/', message_views.compose_message, name='compose_message'),
    path('messages/<int:thread_id>/', message_views.message_detail, name='message_detail'),
    path('messages/<int:thread_id>/reply/', message_views.reply_message, name='reply_message'),
    path('exams/', exam_views.exam_dashboard, name='exam_dashboard'),
    path('exams/add/', exam_views.add_exam, name='add_exam'),
    path('exams/<int:exam_id>/', exam_views.exam_detail, name='exam_detail'),
    path('exams/<int:exam_id>/subjects/add/', exam_views.add_exam_subject, name='add_exam_subject'),
    path('exams/subjects/<int:exam_subject_id>/marks/', exam_views.marks_entry, name='marks_entry'),
    path('exams/<int:exam_id>/results/', exam_views.exam_results, name='exam_results'),
    path('exams/<int:exam_id>/student/<int:student_id>/card/', exam_views.student_result_card, name='student_result_card'),
    path('', include('school.urls')),
]
