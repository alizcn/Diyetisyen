from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'dietitian', 'date', 'time', 'status', 'duration')
    list_filter = ('status', 'date', 'dietitian')
    search_fields = ('patient__first_name', 'patient__last_name', 'dietitian__first_name', 'dietitian__last_name')
    date_hierarchy = 'date'
    ordering = ('-date', '-time')

    fieldsets = (
        ('Randevu Bilgileri', {
            'fields': ('dietitian', 'patient', 'date', 'time', 'duration')
        }),
        ('Durum', {
            'fields': ('status', 'notes')
        }),
    )
