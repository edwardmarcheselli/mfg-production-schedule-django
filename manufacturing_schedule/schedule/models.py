from django.db import models
from projects.models import Projects
from bom.models import BOM, LineItemPart, Parts

# Create your models here.
class Release(models.Model):
    bom = models.ForeignKey(BOM, on_delete=models.CASCADE, related_name="release_bom")
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="release_project", null=True)
    requested_completion_date = models.DateField()
    priority = models.IntegerField(default=-1)
    release_date = models.DateTimeField(auto_now_add=True)
    scheduled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Release"

    def __str__(self):
        return str(self.bom) + ' - ' + str(self.release_date.date()) + ' - ' + str(self.priority)

class ScheduleItems(models.Model):
    schedule_part = models.ForeignKey(Parts,  on_delete=models.CASCADE, related_name="schedule_parts", null=True)
    schedule_line_Item = models.ForeignKey(LineItemPart,  on_delete=models.CASCADE, related_name="schedule_lineitems", null=True)
    schedule_release = models.ForeignKey(Release,  on_delete=models.CASCADE, related_name="schedule_releases", null=True)

    class Routing(models.Choices):
        LASER = 1
        WELD = 2
        PRESS = 3
        MACHINE = 4
        CUT = 5
        PAINT = 6

    routing = models.IntegerField(choices=Routing.choices, null=True, blank=True)
    routing_time = models.IntegerField(null=True, blank=True)
    route_order = models.IntegerField(null=True, blank=True)
    preroute_schedule_item = models.ForeignKey('self',on_delete=models.CASCADE, related_name="schedule_part_reverse", null=True)
    preroute_finish_datetime = models.DateField(null=True, blank=True)
    work_datetime = models.DateField(null=True, blank=True)
    work_finish_datetime = models.DateField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    worker_num = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Schedule Items"

    def __str__(self):
        return str(self.routing) + ' - ' + str(self.schedule_part) + ' - ' + str(self.schedule_release) + ' - ' + str(self.work_datetime)