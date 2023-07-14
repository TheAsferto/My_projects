from django.contrib import admin

# Register your models here.
from .models import User, Student, Teacher, Group

admin.site.register([User, Teacher, Student, Group])
