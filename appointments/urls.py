from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_appointments, name='list_appointments'),
    path('create/', views.patient_appointment_new, name='create_appointment'),
    path('<int:appointment_id>/update/', views.dietitian_appointment_update, name='update_appointment'),
    path('<int:appointment_id>/cancel/', views.patient_appointment_cancel, name='cancel_appointment'),
]
