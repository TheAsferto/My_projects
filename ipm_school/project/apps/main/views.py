from django.contrib.auth import authenticate, login
from django.shortcuts import render

from .forms import StudentCreationForm, TeacherCreationForm


def index(request):
    return render(request, "index.html", {})


def registration_teacher(request):
    if request.method == 'POST':
        form = TeacherCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TeacherCreationForm()

    return render(request, 'authorization/registration_teacher.html', {'form': form})


def registration_student(request):
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = StudentCreationForm()

    return render(request, 'authorization/registration_student.html', {'form': form})


def authorization(request):
    return render(request, "authorization.html", {})


def page_student_lk(request):
    return render(request, "student/page_student_lk.html", {})


def page_teacher_lk(request):
    return render(request, "page_teacher_lk.html", {})


def page_student_class(request):
    return render(request, "page_student_class.html", {})


def page_teacher_class(request):
    return render(request, "page_teacher_class.html", {})


# example
# class Regions(View):
#     def get(self, request):
#         self.regions = [
#             'Москва',
#             'Московская область',
#             'Самарская область',
#             'Chicago, IL'
#         ]
#         return render(request, 'about/regions_GET.html', {'regs': self.regions})
#
#     def post(self, request):
#         self.message = 'Регион успешно создан'
#         return render(request, 'about/regions_POST.html', {'mes': self.message})

def my_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
