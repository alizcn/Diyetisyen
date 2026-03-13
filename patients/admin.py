from django.contrib import admin
from .models import Measurement


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'weight', 'body_fat_percentage', 'bmi')
    list_filter = ('date', 'patient')
    search_fields = ('patient__first_name', 'patient__last_name')
    date_hierarchy = 'date'
    ordering = ('-date',)

    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('patient', 'date')
        }),
        ('Kilo ve Vücut Kompozisyonu', {
            'fields': ('weight', 'body_fat_percentage', 'muscle_mass')
        }),
        ('Vücut Ölçüleri', {
            'fields': ('waist_circumference', 'hip_circumference', 'chest_circumference', 'arm_circumference')
        }),
        ('Notlar', {
            'fields': ('notes',)
        }),
    )

    readonly_fields = ()

    def bmi(self, obj):
        return obj.bmi if obj.bmi else '-'
    bmi.short_description = 'BMI'
