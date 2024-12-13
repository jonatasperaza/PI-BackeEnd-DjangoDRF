from django.db import models

class Grades(models.Model):
    grades = models.JSONField()
    studentInfo = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    photo = models.TextField()

    class Meta:
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'

    def __str__(self):
        return self.grades