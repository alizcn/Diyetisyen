from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_appointments, name='patient_appointments'),
    path('yeni/', views.patient_appointment_new, name='patient_appointment_new'),
    path('<int:appointment_id>/iptal/', views.patient_appointment_cancel, name='patient_appointment_cancel'),
]
