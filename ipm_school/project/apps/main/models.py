from django.db import models


# Create your models here.

# table Teacher of Phisic
class TeacherPh(models.Model):
    techer_ph_ID = models.BigAutoField(primary_key=True)
    mail = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    university = models.CharField(max_length=50)
    faculty = models.CharField(max_length=50)


# table Teacher of Mathematic
class TeacherMath(models.Model):
    techer_math_ID = models.BigAutoField(primary_key=True)
    mail = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    university = models.CharField(max_length=50)
    faculty = models.CharField(max_length=50)


# table Teacher of IT
class TeacherInf(models.Model):
    techer_inf_ID = models.BigAutoField(primary_key=True)
    mail = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    university = models.CharField(max_length=50)
    faculty = models.CharField(max_length=50)


# table group
class Group(models.Model):
    CLASS_NUM = [
        (9, 9),
        (10, 10),
        (11, 11),
    ]

    class_ID = models.BigAutoField(primary_key=True)
    class_name = models.CharField(max_length=50)
    class_number = models.IntegerField(choices=CLASS_NUM)
    TeacherPh_ID = models.ForeignKey(TeacherPh, null=True, on_delete=models.SET_NULL)
    TeacherMath_ID = models.ForeignKey(TeacherMath, null=True, on_delete=models.SET_NULL)
    TeacherInf_ID = models.ForeignKey(TeacherInf, null=True, on_delete=models.SET_NULL)


# table of student
class Student(models.Model):
    CLASS_NUM = [
        (9, 9),
        (10, 10),
        (11, 11),
    ]

    student_ID = models.BigAutoField(primary_key=True)
    mail = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    class_number = models.IntegerField(choices=CLASS_NUM)
    class_ID = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)

# table
