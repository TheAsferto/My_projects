from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
import datetime


# Create your models here.

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        assert extra_fields['is_superuser']
        return self._create_user(email, password, **extra_fields)


# table Teacher
class Teacher(AbstractBaseUser):
    SUBJECT_NAME = [
        ("Информатика", "Информатика"),
        ("Физика", "Физика"),
        ("Математика", "Математика"),
    ]

    last_login = models.DateField(blank=True, null=True, default=datetime.date.today)
    teacher_id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    university = models.CharField(max_length=50)
    faculty = models.CharField(max_length=50)
    subject = models.CharField(choices=SUBJECT_NAME)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"


# table group
class Group(models.Model):
    CLASS_NUM = [
        (9, 9),
        (10, 10),
        (11, 11),
    ]

    class_id = models.BigAutoField(primary_key=True)
    class_name = models.CharField(max_length=50)
    class_number = models.IntegerField(choices=CLASS_NUM)
    teacher_inf_id = models.ForeignKey(Teacher, related_name="teacher_inf", null=True, on_delete=models.SET_NULL)
    teacher_ph_id = models.ForeignKey(Teacher, related_name="teacher_ph", null=True, on_delete=models.SET_NULL)
    teacher_math_id = models.ForeignKey(Teacher, related_name="teacher_math", null=True, on_delete=models.SET_NULL)


# table of student
class Student(AbstractBaseUser, PermissionsMixin):
    CLASS_NUM = [
        (9, 9),
        (10, 10),
        (11, 11),
    ]

    last_login = models.DateField(blank=True, null=True, default=datetime.date.today)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    student_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    class_number = models.IntegerField(choices=CLASS_NUM, null=True)
    class_ID = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []
