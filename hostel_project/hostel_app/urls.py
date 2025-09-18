# hostel_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("student/<int:student_id>/", views.student_detail, name="student_detail"),
    path("student/<int:student_id>/messcut/", views.add_messcut, name="add_messcut"),
    path("student/<int:student_id>/icecream/", views.add_icecream, name="add_icecream"),
    path("fees/", views.fees_list, name="fees_list"),
    path('add_student/', views.add_student, name='add_student'),
    path("delete-student/", views.delete_student_page, name="delete_student_page"),
    path("delete-student/<int:student_id>/", views.delete_student, name="delete_student"),
    path('add-icecream/', views.add_icecream_global, name='add_icecream_global'),
    path('student/<int:student_id>/add-icecream/', views.add_icecream, name='add_icecream'),
    path('list-icecream/', views.list_icecream, name='list_icecream'),
    ]
