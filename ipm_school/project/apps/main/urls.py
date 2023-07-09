from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration_teacher/', views.registration_teacher, name='registration_teacher'),
    path('registration_student/', views.registration_student, name='registration_student'),
    path('authorization/', views.authorization, name='authorization'),
    path('page_student_lk/', views.page_student_lk, name='page_student_lk'),
    path('page_teacher_lk/', views.page_teacher_lk, name='page_teacher_lk'),
    path('page_student_class/', views.page_student_class, name='page_student_class'),
    path('page_teacher_class/', views.page_teacher_class, name='page_teacher_class'),
]