from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import User
from django.contrib.auth import views as auth_views
from .forms import StudentSignUpForm, TeacherSignUpForm, LoginForm
from django.urls import reverse
from .decorators import student_required, teacher_required
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html", {})


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
    context = {}
    return render(request, 'index.html', context)


def update_authorization(request):
    return render(request, "authorization/update_authorization.html", {})


def page_student_class(request):
    return render(request, "page_student_class.html", {})


def page_teacher_class(request):
    return render(request, "page_teacher_class.html", {})

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
