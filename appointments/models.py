from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Planlandı'),
        ('confirmed', 'Onaylandı'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi'),
    )

    dietitian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dietitian_appointments',
        limit_choices_to={'user_type': 'dietitian'},
        verbose_name='Diyetisyen'
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_appointments',
        limit_choices_to={'user_type': 'patient'},
        verbose_name='Hasta'
    )
    date = models.DateField(verbose_name='Tarih')
    time = models.TimeField(verbose_name='Saat')
    duration = models.PositiveIntegerField(default=30, verbose_name='Süre (dakika)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name='Durum')
    notes = models.TextField(blank=True, verbose_name='Notlar')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Randevu'
        verbose_name_plural = 'Randevular'
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.patient.full_name} - {self.dietitian.full_name} ({self.date} {self.time})"

    def clean(self):
        # Geçmiş tarihlere randevu oluşturulmasını engelle
        if self.date and self.date < timezone.now().date():
            raise ValidationError('Geçmiş tarihlere randevu oluşturamazsınız.')

        # Aynı diyetisyen için çakışan randevu kontrolü
        if self.dietitian and self.date and self.time:
            conflicting = Appointment.objects.filter(
                dietitian=self.dietitian,
                date=self.date,
                time=self.time,
                status__in=['scheduled', 'confirmed']
            ).exclude(pk=self.pk)

            if conflicting.exists():
                raise ValidationError('Bu tarih ve saatte diyetisyenin başka bir randevusu var.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
