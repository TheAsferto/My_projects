from django.contrib import admin

# Register your models here.
from .models import Student, Teacher, Group

admin.site.register([Teacher, Group, Student])
