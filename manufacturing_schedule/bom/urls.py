from django.urls import path
from . import views

urlpatterns = [
    path('bom_upload/', views.bom_upload, name='bom_upload'),
] 