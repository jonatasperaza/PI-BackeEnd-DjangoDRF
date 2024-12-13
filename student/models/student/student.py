from django.db import models
from django.contrib.auth.models import User

class Student(User):
    enrollment = models.CharField(max_length=20)
    course = models.CharField(max_length=100)
    photo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.enrollment