from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "index.html", {})

def registration_teacher(request):
    return render(request, "registration_teacher.html", {})

def registration_student(request):
    return render(request, "registration_student.html", {})

def authorization(request):
    return render(request, "authorization.html", {})

def page_student_lk(request):
    return render(request, "page_student_lk.html", {})

def page_teacher_lk(request):
    return render(request, "page_teacher_lk.html", {})

def page_student_class(request):
    return render(request, "page_student_class.html", {})

def page_teacher_class(request):
    return render(request, "page_teacher_class.html", {})