from django.contrib import admin
from .models import Release, ScheduleItems

# Register your models here.
admin.site.register(Release)
admin.site.register(ScheduleItems)