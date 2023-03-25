from django.db import models

# Create your models here.
class Projects(models.Model):
    project_name = models.CharField()
    project_num = models.CharField()
    