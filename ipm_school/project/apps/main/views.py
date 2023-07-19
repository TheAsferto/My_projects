from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import User, Teacher
from django.contrib.auth import views as auth_views
from .forms import StudentSignUpForm, TeacherSignUpForm, LoginForm
from django.urls import reverse
from .decorators import student_required, teacher_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from . import forms as myforms
#from django.core.files.storage import default_storage
from django.core.files import File
from os.path import basename
import urllib

def index(request):
    if request.user.is_authenticated:
        mail = request.user.email
        teacher_name = Teacher.objects.get(user__email__contains=mail).name
        if request.user.teacher.avatar == '-':
            ava_path = 'avatars/no_ava.png'
        else:
            ava_path = request.user.teacher.avatar
        context = {'name':teacher_name, 'ava_path':ava_path}
    else:
        context = {}
    return render(request, "index.html", context)


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'authorization/registration_teacher.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('authorization')


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'authorization/registration_student.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('authorization')


class LoginView(auth_views.LoginView):
    template_name = 'authorization/authorization.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_student:
                return reverse('page_student_lk')
            if user.is_teacher:
                return reverse('page_teacher_lk')
        else:
            return reverse('authorization')


@login_required
@student_required
def page_student_lk(request):
    context = {}
    return render(request, 'student/page_student_lk.html', context)


@login_required
@teacher_required
def page_teacher_lk(request):
    if request.user.teacher.avatar == '-':
        ava_path = 'avatars/no_ava.png'
    else:
         ava_path = request.user.teacher.avatar
    if request.method == 'POST':
        if 'fathername_frm' in request.POST:
            form = myforms.Fathername_changing_form(request.POST)
            if form.is_valid():
                request.user.teacher.fathername = form.cleaned_data['fathername']
                request.user.teacher.save()
        if 'name_frm' in request.POST:
            form = myforms.Name_changing_form(request.POST)
            if form.is_valid():
                request.user.teacher.name = form.cleaned_data['name']
                request.user.teacher.save()
        if 'surn_frm' in request.POST:
            form = myforms.Surn_changing_form(request.POST)
            if form.is_valid():
                request.user.teacher.surname = form.cleaned_data['surname']
                request.user.teacher.save()
        if 'tel_frm' in request.POST:
            form = myforms.Tel_changing_form(request.POST)
            if form.is_valid():
                request.user.teacher.phone_number = form.cleaned_data['phone']
                request.user.teacher.save()
        if 'class_frm' in request.POST:
            form = myforms.Class_changing_form(request.POST)
            if form.is_valid():
                request.user.teacher.teacher_class_num = form.cleaned_data['tclass']
                request.user.teacher.save()
        if 'avatar' in request.FILES:
            file = request.FILES['avatar']
            ava_model = request.user.teacher
            ava_model.avatar.delete()
            ava_model.avatar = request.FILES['avatar']
            ava_model.save()
            ava_path = request.user.teacher.avatar

    context = { 'email':request.user.email,
                'name':request.user.teacher.name,
                'surname':request.user.teacher.surname, 
                'fathername':request.user.teacher.fathername,
                'phone': request.user.teacher.phone_number,
                'tclass': request.user.teacher.teacher_class_num, 
                'ava_path': ava_path,}
    return render(request, 'teacher/page_teacher_lk.html', context)


def update_authorization(request):
    return render(request, "authorization/update_authorization.html", {})


def page_student_class(request):
    return render(request, "page_student_class.html", {})


def page_teacher_class(request):
    return render(request, "page_teacher_class.html", {})

def logout(request):
    logout(request) 
    return redirect('index')

# def my_view(request):
#     username = request.POST["username"]
#     password = request.POST["password"]
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         ...
#     else:
#         # Return an 'invalid login' error message.
#         ...
