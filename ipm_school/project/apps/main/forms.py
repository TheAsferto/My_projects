from django import forms
from django.core.exceptions import ValidationError
from . import models


class CreationForm(forms.ModelForm):
    email = forms.CharField(label="email")
    password1 = forms.CharField(label="password1")
    password2 = forms.CharField(label="password2")

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class StudentCreationForm(CreationForm):
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if email and models.Student.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    class Meta:
        model = models.Student
        fields = ["email", "name", "surname", "class_number"]


class TeacherCreationForm(CreationForm):
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if email and models.Teacher.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    class Meta:
        model = models.Teacher
        fields = ["email", "name", "surname", "university", "faculty", "subject"]
