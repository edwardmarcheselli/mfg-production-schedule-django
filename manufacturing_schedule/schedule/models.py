from django.db import models
from bom.models import BOM
from projects.models import Projects

# Create your models here.
class Release(models.Model):
    bom = models.ForeignKey(BOM, on_delete=models.CASCADE, related_name="boms")
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="projects")
    requested_completion_date = models.DateField()
    priority = models.IntegerField(default=-1)
    release_date = models.DateField()

    class Meta:
        verbose_name = "Release"