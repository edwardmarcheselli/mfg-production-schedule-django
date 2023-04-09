from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.schedule_display, name='schedule_display'),
    path('create_release/', views.create_release, name='create_release'),
] 