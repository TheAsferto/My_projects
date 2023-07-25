import jwt
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from .models import User, Teacher, Student, Group
from django.contrib.auth import views as auth_views
from .forms import StudentSignUpForm, TeacherSignUpForm, EmailVerification, LoginForm, SetNewPasswordForm, \
    ResetPasswordEmailForm, StudentForm
from django.urls import reverse
from .decorators import student_required, teacher_required
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .emails import Util
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponse
from . import forms as myforms
from django.http import HttpResponsePermanentRedirect
import os
from rest_framework.exceptions import AuthenticationFailed


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


def signupformvalid(self, form):
    user = form.save()
    user_email = form.cleaned_data['email']
    user_name = form.cleaned_data['name']
    tokens = RefreshToken.for_user(user).access_token
    current_site = get_current_site(self.request).domain
    relative_link = reverse('email-verify')
    abs_url = 'http://' + current_site + relative_link + "?token=" + str(tokens)
    email_body = 'Здравствуйте, ' + user_name + \
                 '.\nПодтвердите свою почту, перейдя по ссылке ниже: \n' + abs_url
    data = {'email_body': email_body, 'to_email': user_email,
            'email_subject': 'Verify your email'}

    Util.send_email(data=data)

    return user_email


def index(request):
    if request.user.is_authenticated:
        mail = request.user.email
        if request.user.is_teacher:
            teacher_name = Teacher.objects.get(user__email__contains=mail).name
            if request.user.teacher.avatar == '-':
                ava_path = 'avatars/no_ava.png'
            else:
                ava_path = request.user.teacher.avatar
            context = {'name':teacher_name, 'ava_path':ava_path}
        if request.user.is_student:
            student_name = Student.objects.get(user__email__contains=mail).name
#           if request.user.student.avatar == '-':
            ava_path = 'avatars/no_ava.png'
#           else:
#           ava_path = request.user.teacher.avatar
            context = {'name':student_name, 'ava_path':ava_path}
            print('студент ', student_name)
            context = {'name':student_name, 'ava_path':ava_path}
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
        user_email = signupformvalid(self, form)

        return HttpResponse('Для входа в аккаунт необходимо перейти по ссылке, которую вы получили на указанную '
                            'электронную почту,' + user_email + '.', status=200)


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'authorization/registration_student.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user_email = signupformvalid(self, form)

        return HttpResponse('Для входа в аккаунт необходимо перейти по ссылке, которую вы получили на указанную '
                            'электронную почту, ' + user_email + '.', status=200)


class VerifyEmail(CreateView):
    form_class = EmailVerification

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return redirect('authorization')
        except jwt.ExpiredSignatureError:
            return HttpResponse('Activation Expired', status=400)
        except jwt.exceptions.DecodeError:
            return HttpResponse('Invalid token', status=400)


class ResetPassword(CreateView):
    template_name = 'authorization/reset_password_email.html'
    form_class = ResetPasswordEmailForm

    def post(self, request):
        form = ResetPasswordEmailForm(request.POST)
        user_email = form.data['email']
        if User.objects.filter(email=user_email).exists():
            user = User.objects.get(email=user_email)

            if user.is_teacher:
                teacher = Teacher.objects.get(user_id=user.id)
                user_name = teacher.name
            elif user.is_student:
                student = Student.objects.get(user_id=user.id)
                user_name = student.name

            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=self.request).domain
            realtivelink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + realtivelink
            email_body = 'Здравствуйте, ' + user_name + '.\nИспользуйте ссылку ниже для восстановления пароля: \n' + \
                         absurl
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your password'}
            Util.send_email(data)
            return HttpResponse('Для дальнейшей смены пароля необходимо перейти по ссылке, которую вы получили '
                                'на указанную электронную почту, ' + user_email)
        return HttpResponse('Аккаунтов зарегестрированных на почту' + user_email + ' не существует.', status=401)


class PasswordTokenCheck(CreateView):
    form_class = SetNewPasswordForm

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return HttpResponse('token is not valid, please check the new one', status=401)
            return CustomRedirect(request.build_absolute_uri('/password-reset-complete' +
                                                             '?token_valid=True&'
                                                             'message=Credentials Valid&'
                                                             'uidb64=' + uidb64 +
                                                             '&token=' + token))
        except DjangoUnicodeDecodeError as indentifier:
            return HttpResponse('token is not valid, please check the new one', status=401)


class SetNewPassword(CreateView):
    model = User
    template_name = 'authorization/reset_password_complete.html'
    form_class = SetNewPasswordForm

    def post(self, request):
        try:
            form = self.form_class(request.POST)
            password = form.data['password2']
            token = request.GET.get('token', "")
            uidb64 = request.GET.get('uidb64', "")
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            print(form.is_valid())
            if form.is_valid():
                user.set_password(password)
                user.save()
                return HttpResponse('Password is reset successfully', status=200)
                # return reverse('authorization')
            else:
                print('пароли не совпадают')
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)


class LoginView(auth_views.LoginView):
    template_name = 'authorization/authorization.html'
    form_class = LoginForm

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
    profile_id = request.user.id
    email = request.user.email
    user = Student.objects.get(user__id__contains=profile_id)
    group_id = user.group_id
    subjects = []
    if group_id:
        group = Group.objects.get(class_id__contains=group_id)
        if group.teacher_math:
            subjects.append('Математика')
        if group.teacher_ph:
            subjects.append('Физика')
        if group.teacher_inf:
            subjects.append('Информатика')
    if user.avatar == '-':
        user.avatar = 'avatars/no_ava.png'
    context = {'profile_id': profile_id, 'user': user, 'email': email, 'subjects': subjects}
    if not user.group_id:
        return render(request, 'student/page_student_lk_no_class.html', context)
    return render(request, 'student/page_student_lk.html', context)


def student_join_group(request):
    profile_id = request.user.id
    user = Student.objects.get(user__id__contains=profile_id)
    groups = Group.objects.filter(class_number=request.user.student.class_number)
    for row in groups:
        user.group_id = row.class_id
        user.save()
        break
    return redirect('page_student_lk')


class StudentEditFormView(View):
    def get(self, request, profile_id):
        user = Student.objects.get(user__id__contains=profile_id)
        user_form = StudentForm(instance=user)
        context = {'user_form': user_form, 'profile_id': profile_id}
        return render(request, 'student/page_student_lk_edit.html', context)

    def post(self, request, profile_id):
        user = Student.objects.get(user__id__contains=profile_id)
        user.surname = request.POST.get('surname')
        user.name = request.POST.get('name')
        user.fathername = request.POST.get('fathername')
        user.phone_number = request.POST.get('phone_number')
        user.class_number = request.POST.get('class_number')
        user.save()
        return redirect('page_student_lk')


#функция записи в группу
def teach_join_group(request, my_cl):
    global gr_id
    #нужно для вывода class_id и записи в группу
    subj = request.user.teacher.subject
    if subj == 'Информатика':
        kwarg = {  '{}'.format('teacher_inf_id'): None}
        field = 'teacher_inf'
        kwarg1 = {  '{}'.format('teacher_inf_id'): request.user.id}
    elif subj == 'Физика':
        kwarg = {  '{}'.format('teacher_ph_id'): None}
        field = 'teacher_ph'
        kwarg1 = {  '{}'.format('teacher_ph_id'): request.user.id}
    elif subj == 'Математика':
        kwarg = {  '{}'.format('teacher_math_id'): None}
        field = 'teacher_math'
        kwarg1 = {  '{}'.format('teacher_math_id'): request.user.id}
    #количество групп в которых состоит препод
    my_gr = Group.objects.filter(**kwarg1)
    #ловим запрос на поиск
    if request.method == 'POST':
        if 't_gr_search' in request.POST:
            print("Принят запрос на поиск группы")
            if my_gr.count() == 0 and my_cl: #допускаем к записи только тех, кто еще не записан
                groups = Group.objects.filter(**kwarg, class_number=request.user.teacher.teacher_class_num)
                print("Найдено групп:" ,groups.count())
                if groups.count()>0:
                    for row in groups:
                        kwarg2 = {'class_id': row.class_id}
                        k = 0
                        if row.teacher_inf_id != None:
                            k += 1
                        if row.teacher_ph_id != None:
                            k += 1
                        if row.teacher_math_id != None:
                            k += 1
                        if k == 2:
                            print(f'Обнаружена группа (id: {row.class_id}) с двумя преподами - начинаю запись')
                            g = Group(**kwarg1, **kwarg2,)
                            g.save(update_fields=[field])
                            break
                        elif k == 1:
                            print('Обнаружена группа с одним преподом - начинаю запись')
                            g = Group(**kwarg1, **kwarg2,)
                            g.save(update_fields=[field])
                            break
                else:
                    print('Групп без преподавателя не найдено - создаю новою группу')
                    g = Group(**kwarg1, class_number=request.user.teacher.teacher_class_num)
                    g.save()
            elif my_gr == 1:
                print(f'Вы уже состоите в группе (id: {Group.objects.get(**kwarg1).class_number})')
                #изменение выбранного класса для преподования на класс вашей группы
                if request.user.teacher.teacher_class_num != Group.objects.get(**kwarg1).class_number:
                    request.user.teacher.teacher_class_num = Group.objects.get(**kwarg1).class_number
                    request.user.teacher.save(update_fields=['teacher_class_num'])
        if 'ex_gr' in request.POST:
            print("Принят запрос на выход из группы")
            if my_gr.count() > 0:
                row = Group.objects.get(**kwarg1)
                k = 0
                if row.teacher_inf_id != None:
                    k += 1
                if row.teacher_ph_id != None:
                    k += 1
                if row.teacher_math_id != None:
                    k += 1
                if k == 1:
                    g = Group.objects.get(**kwarg1).delete()
                else:
                    kwarg2 = {'class_id': row.class_id}
                    g = Group(**kwarg, **kwarg2)
                    g.save(update_fields=[field])
    #флаг участия в группе
    gr_id = Group.objects.get(**kwarg1).class_id if Group.objects.filter(**kwarg1).count()==1 else None


@login_required
@teacher_required
def page_teacher_lk(request):
    #для вывода авы
    if request.user.teacher.avatar == '-':
        ava_path = 'avatars/no_ava.png'
    else:
         ava_path = request.user.teacher.avatar
    #проверка заполнен ли класс для препода
    my_cl = request.user.teacher.teacher_class_num
    cl_ch= True if my_cl in (9,10,11) else False
    #функция записи в группу
    teach_join_group(request, my_cl)
    context = { 'email':request.user.email,
                'name':request.user.teacher.name,
                'surname':request.user.teacher.surname,
                'fathername':request.user.teacher.fathername,
                'phone': request.user.teacher.phone_number,
                'tclass': request.user.teacher.teacher_class_num,
                'ava_path': ava_path,
                'gr_id': gr_id,
                'cl_ch': cl_ch}
    return render(request, 'teacher/page_teacher_lk.html', context)

@login_required
@teacher_required
def page_teach_settings(request):
    #для вывода авы
    if request.user.teacher.avatar == '-':
        ava_path = 'avatars/no_ava.png'
    else:
         ava_path = request.user.teacher.avatar
    #ловим разные запросы
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
            if request.POST['tclass'] is not None:
                form = myforms.Class_changing_form(request.POST)
                if form.is_valid():
                    request.user.teacher.teacher_class_num = form.cleaned_data['tclass']
                    request.user.teacher.save()
                    cl_ch = True
        if 'avatar' in request.FILES:
            file = request.FILES['avatar']
            ava_model = request.user.teacher
            ava_model.avatar.delete()
            ava_model.avatar = request.FILES['avatar']
            ava_model.save()
            ava_path = request.user.teacher.avatar

    #проверка заполнен ли класс для препода
    my_cl = request.user.teacher.teacher_class_num
    cl_ch= True if my_cl in (9,10,11) else False
    #функция записи в группу
    teach_join_group(request, my_cl)
    context = { 'email':request.user.email,
                'name':request.user.teacher.name,
                'surname':request.user.teacher.surname,
                'fathername':request.user.teacher.fathername,
                'phone': request.user.teacher.phone_number,
                'tclass': request.user.teacher.teacher_class_num,
                'ava_path': ava_path,
                'gr_id': gr_id,
                'cl_ch': cl_ch}
    return render(request, 'teacher/page_teach_settings.html', context)



def update_authorization(request):
    return render(request, "authorization/reset_password_email.html", {})


def page_student_class(request):
    global teacher_inf, teacher_ph, teacher_math
    profile_id = request.user.id
    user = Student.objects.get(user__id__contains=profile_id)
    group_id = user.group_id
    group = Group.objects.get(class_id__contains=group_id)
    subjects = []
    teachers = []
    if group.teacher_math:
        teacher_math = Teacher.objects.get(user__id__contains=group.teacher_math_id)
        subjects.append('Математика')
        teachers.append(teacher_math)
    if group.teacher_ph:
        teacher_ph = Teacher.objects.get(user__id__contains=group.teacher_ph_id)
        subjects.append('Физика')
        teachers.append(teacher_ph)
    if group.teacher_inf:
        teacher_inf = Teacher.objects.get(user__id__contains=group.teacher_inf_id)
        subjects.append('Информатика')
        teachers.append(teacher_inf)
    context = {
        'profile_id': profile_id,
        'user': user,
        'subjects': subjects,
        'teachers': teachers
    }
    return render(request, "student/page_student_class.html", context)


def page_teacher_class(request):
    return render(request, "page_teacher_class.html", {})


def logout(request):
    logout(request)
    return redirect('index')
