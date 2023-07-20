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


class User(AbstractBaseUser, PermissionsMixin):
    last_login = models.DateField(blank=True, null=True, default=datetime.date.today)

    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"


class Teacher(AbstractBaseUser):
    CLASS_NUM = [
        (9, 9),
        (10, 10),
        (11, 11),
    ]
    SUBJECT_NAME = [
        ("Информатика", "Информатика"),
        ("Физика", "Физика"),
        ("Математика", "Математика"),
    ]

    last_login = models.DateField(blank=True, null=True, default=datetime.date.today)

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='teacher')
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    university = models.CharField(max_length=50)
    faculty = models.CharField(max_length=50)
    subject = models.CharField(choices=SUBJECT_NAME)
    is_superuser = models.BooleanField(default=False)
    fathername = models.CharField(max_length=50, default='-')
    phone_number = models.CharField(max_length=20, default='-')
    avatar = models.ImageField(upload_to="avatars/", default='-')
    teacher_class_num = models.IntegerField(choices=CLASS_NUM, null=True)

    objects = CustomUserManager()


class Group(models.Model):
    CLASS_NUM = [
        (9, 9),
        (10, 10),
        (11, 11),
    ]

    class_id = models.BigAutoField(primary_key=True)
    class_name = models.CharField(max_length=50)
    class_number = models.IntegerField(choices=CLASS_NUM)
    teacher_inf = models.ForeignKey(Teacher, related_name="teacher_inf", null=True, on_delete=models.SET_NULL)
    teacher_ph = models.ForeignKey(Teacher, related_name="teacher_ph", null=True, on_delete=models.SET_NULL)
    teacher_math = models.ForeignKey(Teacher, related_name="teacher_math", null=True, on_delete=models.SET_NULL)


class Student(AbstractBaseUser):
    CLASS_NUM = [
        (9, 9),
        (10, 10),
        (11, 11),
    ]

    last_login = models.DateField(blank=True, null=True, default=datetime.date.today)

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    class_number = models.IntegerField(choices=CLASS_NUM, null=True)
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)

    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
