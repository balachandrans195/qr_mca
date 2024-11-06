from datetime import date, timezone
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=50)

    def str(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    semester = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)  # Optional date field


    def str(self):
        return f"{self.name} - Sem {self.semester}"


class Student(models.Model):
    name = models.CharField(max_length=200)
    register_number = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    college_name = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    dob = models.DateField()
    password = models.CharField(max_length=100)

    def str(self):
        return self.name


class Admin(models.Model):
    name = models.CharField(max_length=200)
    admin_number = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Invigilator(models.Model):
    name = models.CharField(max_length=200)
    invigilator_number = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester_number = models.IntegerField()
    subjects = models.TextField()  # Store subject names as a comma-separated string
    payment_date = models.DateTimeField(auto_now_add=True)  # Automatically set to now when the object is created
    payment_successful = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"Payment for {self.student.name} - Semester {self.semester_number}"