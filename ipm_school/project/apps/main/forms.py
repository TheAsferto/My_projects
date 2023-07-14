from django import forms
from django.core.exceptions import ValidationError
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction

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
