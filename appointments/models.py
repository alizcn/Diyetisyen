from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', _('Planlandı')),
        ('confirmed', _('Onaylandı')),
        ('completed', _('Tamamlandı')),
        ('cancelled', _('İptal Edildi')),
    )

    dietitian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dietitian_appointments',
        limit_choices_to={'user_type': 'dietitian'},
        verbose_name=_('Diyetisyen')
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_appointments',
        limit_choices_to={'user_type': 'patient'},
        verbose_name=_('Hasta')
    )
    date = models.DateField(verbose_name=_('Tarih'))
    time = models.TimeField(verbose_name=_('Saat'))
    duration = models.PositiveIntegerField(default=30, verbose_name=_('Süre (dakika)'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name=_('Durum'))
    notes = models.TextField(blank=True, verbose_name=_('Notlar'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Randevu')
        verbose_name_plural = _('Randevular')
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.patient.full_name} - {self.dietitian.full_name} ({self.date} {self.time})"

    def clean(self):
        # Geçmiş tarihlere randevu oluşturulmasını engelle
        if self.date and self.date < timezone.now().date():
            raise ValidationError(_('Geçmiş tarihlere randevu oluşturamazsınız.'))

        # Aynı diyetisyen için çakışan randevu kontrolü
        if self.dietitian and self.date and self.time:
            conflicting = Appointment.objects.filter(
                dietitian=self.dietitian,
                date=self.date,
                time=self.time,
                status__in=['scheduled', 'confirmed']
            ).exclude(pk=self.pk)

            if conflicting.exists():
                raise ValidationError(_('Bu tarih ve saatte diyetisyenin başka bir randevusu var.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
