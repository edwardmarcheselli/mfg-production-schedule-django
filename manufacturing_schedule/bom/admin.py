from django.contrib import admin
from .models import Parts, LineItemPart, BOM

# Register your models here.
admin.site.register(Parts)
admin.site.register(LineItemPart)
admin.site.register(BOM)