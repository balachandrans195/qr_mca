from django.urls import path

from . import views
from .views import DepartmentAPI, SubjectAPI, StudentAPI, AdminAPI, InvigilatorAPI, LoginAPI, RegisterStudentView, \
    payment_handler, cash_payment, student_payments_view

urlpatterns = [
    path('departments/', DepartmentAPI.as_view(), name='department-api'),
    path('subjects/', SubjectAPI.as_view(), name='subject-api'),
    path('students/', StudentAPI.as_view(), name='student-api'),
    path('admins/', AdminAPI.as_view(), name='admin-api'),
    path('invigilators/', InvigilatorAPI.as_view(), name='invigilator-api'),

    # Include a route for accessing by id
    path('departments/<int:id>/', DepartmentAPI.as_view(), name='department-detail'),
    path('subjects/<int:id>/', SubjectAPI.as_view(), name='subject-detail'),
    path('students/<int:id>/', StudentAPI.as_view(), name='student-detail'),
    path('admins/<int:id>/', AdminAPI.as_view(), name='admin-detail'),
    path('invigilators/<int:id>/', InvigilatorAPI.as_view(), name='invigilator-detail'),

    # Add the login endpoint
    path('login/', LoginAPI.as_view(), name='login-api'),
    path('register/', RegisterStudentView.as_view(), name='register_student'),

    path('payments/<int:student_id>/', payment_handler, name='payment_handler'),

    path('api/cash-payment/<int:student_id>/', cash_payment, name='cash_payment'),

    path('api/student-payments/', student_payments_view, name='student_payments_view'),
    path('api/student-payments/<int:payment_id>/', views.student_payments_view, name='student_payment_detail'),  # For PUT and DELETE

]
