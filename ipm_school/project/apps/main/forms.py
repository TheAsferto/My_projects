from django import forms
from django.core.exceptions import ValidationError
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import Student
import re

User = get_user_model()


class TeacherSignUpForm(forms.ModelForm):
    email = forms.CharField(label="email")
    password1 = forms.CharField(label="password1")
    password2 = forms.CharField(label="password2")

    name = forms.CharField(label='name')
    surname = forms.CharField(label='surname')
    university = forms.CharField(label='university')
    faculty = forms.CharField(label='faculty')
    subject = forms.CharField(label='subject')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if email and models.User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        teacher = models.Teacher.objects.create(user=user,
                                                name=self.cleaned_data.get('name'),
                                                surname=self.cleaned_data.get('surname'),
                                                university=self.cleaned_data.get('university'),
                                                faculty=self.cleaned_data.get('faculty'),
                                                subject=self.cleaned_data.get('subject'))
        return user


class StudentSignUpForm(forms.ModelForm):
    email = forms.CharField(label="email")
    password1 = forms.CharField(label="password1")
    password2 = forms.CharField(label="password2")

    name = forms.CharField(label='name')
    surname = forms.CharField(label='surname')
    class_number = forms.IntegerField(label='class_number')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if email and models.User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        student = models.Student.objects.create(user=user,
                                                name=self.cleaned_data.get('name'),
                                                surname=self.cleaned_data.get('surname'),
                                                class_number=self.cleaned_data.get('class_number'))
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control rounded-5',
               'id': 'floatingInputEmail'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control rounded-5',
               'style': 'margin-bottom: 0px;'}))


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        exclude = ['last_login', 'password', 'user', 'is_superuser', 'group', 'avatar']

class Fathername_changing_form(forms.Form):
    fathername = forms.CharField(label='fathername')
    def clean_fathername(self):
        data = self.cleaned_data['fathername']
        if bool(re.search('[A-zA-Z]', data)):
            print("В отчестве использована латиница")
            raise ValidationError("В отчестве использована латиница")
        return data

class Name_changing_form(forms.Form):
    name = forms.CharField(label='name')
    def clean_name(self):
        data = self.cleaned_data['name']
        if bool(re.search('[A-zA-Z]', data)):
            print("В имени использована латиница")
            raise ValidationError("В имени использована латиница")
        return data

class Surn_changing_form(forms.Form):
    surname = forms.CharField(label='surname')
    def clean_surname(self):
        data = self.cleaned_data['surname']
        if bool(re.search('[A-zA-Z]', data)):
            print("В фамилии использована латиница")
            raise ValidationError("В фамилии использована латиница")
        return data

def check_phone(string):
        pattern1 = re.compile('^[78]?[\s]?[\-\s\(]?\d{3}[\-\s\)]?[\s]?\d{3}\-?\d{2}\-?\d{2}$')
        pattern2 = re.compile('^\+(?=7)7[\s]?[\-\s\(]?\d{3}[\-\s\)]?[\s]?\d{3}\-?\d{2}\-?\d{2}$')
        if pattern1.findall(string) or pattern2.findall(string):
            return True
        else:
            return False
class Tel_changing_form(forms.Form):
    phone = forms.CharField(label='phone')
    def clean_phone(self):
        data = self.cleaned_data['phone']
        if not check_phone(data):
            print("Номер не прошел проверку")
            raise ValidationError("Номер не прошел проверку")
        return data

class Class_changing_form(forms.Form):
    tclass = forms.CharField(label='tclass')
    def clean_tclass(self):
        data = self.cleaned_data['tclass']
        if data in (9, 10, 11):
            print("Класс не прошел проверку")
            raise ValidationError("Класс не прошел проверку")
        return data