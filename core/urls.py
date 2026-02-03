from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),
    path('register/', views.register),
    path('admin-dashboard/', views.admin_dashboard),
    path('students/', views.manage_students),
    path('courses/', views.manage_courses),
    path('exams/', views.manage_exams),
    path('marks/', views.add_marks),
    path('student-dashboard/', views.student_dashboard),
    path('upcoming/', views.upcoming_exams),
    path('view-marks/', views.view_marks),
    path('delete-student/<int:id>/', views.delete_student),
    path('delete-course/<int:id>/', views.delete_course),
    path('delete-exam/<int:id>/', views.delete_exam),
    path('delete-mark/<int:id>/', views.delete_mark),
]
