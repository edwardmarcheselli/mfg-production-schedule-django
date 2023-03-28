from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule_display, name='schedule_display'),
] 