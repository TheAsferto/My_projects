from django.contrib import admin

# Register your models here.
from .models import Student, TeacherPh, TeacherInf, TeacherMath, Group

admin.site.register([TeacherPh, TeacherInf, TeacherMath, Group, Student])
