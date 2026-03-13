from django.urls import path
from . import views

urlpatterns = [
    path('', views.dietitian_appointments, name='dietitian_appointments'),
    path('<int:appointment_id>/guncelle/', views.dietitian_appointment_update, name='dietitian_appointment_update'),
    path('<int:appointment_id>/iptal/', views.dietitian_appointment_cancel, name='dietitian_appointment_cancel'),
]
