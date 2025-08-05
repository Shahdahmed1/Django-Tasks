from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    joined_at = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='students/', blank=True, null=True)
    courses = models.ManyToManyField(Course)
