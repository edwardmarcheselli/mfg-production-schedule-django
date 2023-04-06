from django.urls import path
from . import views

app_name = 'bom'

urlpatterns = [
    path('bom_upload/', views.bom_upload, name='bom_upload'),
] 