from django.db import models
from bom.models import BOM
from projects.models import Projects
from bom.models import Parts

# Create your models here.
class Release(models.Model):
    bom = models.ForeignKey(BOM, on_delete=models.CASCADE, related_name="boms")
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="projects", null=True)
    requested_completion_date = models.DateField()
    priority = models.IntegerField(default=-1)
    release_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Release"

    def __str__(self):
        return str(self.bom) + ' - ' + str(self.release_date) + ' - ' + str(self.priority)

class ScheduleItems(models.Model):
    part = models.ForeignKey(Parts,  on_delete=models.CASCADE, related_name="schedule_parts")

    class Routing(models.Choices):
        LASER = 1
        WELD = 2
        PRESS = 3
        MACHINE = 4
        CUT = 5
        PAINT = 6

    routing = models.IntegerField(choices=Routing.choices, null=True, blank=True)
    preroute_finish_datetime = models.DateTimeField(null=True, blank=True)
    work_datetime = models.DateTimeField(null=True, blank=True)
    work_finish_datetime = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)