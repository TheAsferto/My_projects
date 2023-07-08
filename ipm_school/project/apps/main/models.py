from django.db import models


# Create your models here.

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
    # class_ID = models.ForeignKey(Group, on_delete=models.SET_NULL)

#сущность учителя
