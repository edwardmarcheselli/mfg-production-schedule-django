from django.db import models

# Create your models here.
class Projects(models.Model):
    project_name = models.CharField(max_length=30)
    project_num = models.CharField(max_length=30)
