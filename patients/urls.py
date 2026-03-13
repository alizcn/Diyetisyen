from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_progress, name='patient_progress'),
    path('ekle/', views.patient_add_measurement, name='patient_add_measurement'),
]
