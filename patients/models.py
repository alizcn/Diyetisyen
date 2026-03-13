from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Measurement(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='measurements',
        limit_choices_to={'user_type': 'patient'},
        verbose_name=_('Hasta')
    )
    date = models.DateField(verbose_name=_('Tarih'))
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Kilo (kg)'))
    body_fat_percentage = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name=_('Yağ Oranı (%)')
    )
    muscle_mass = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Kas Kütlesi (kg)')
    )
    waist_circumference = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name=_('Bel Çevresi (cm)')
    )
    hip_circumference = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name=_('Kalça Çevresi (cm)')
    )
    chest_circumference = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name=_('Göğüs Çevresi (cm)')
    )
    arm_circumference = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name=_('Kol Çevresi (cm)')
    )
    notes = models.TextField(blank=True, verbose_name=_('Notlar'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Ölçüm')
        verbose_name_plural = _('Ölçümler')
        ordering = ['-date']
        unique_together = ['patient', 'date']

    def __str__(self):
        return f"{self.patient.full_name} - {self.date} ({self.weight} kg)"

    @property
    def bmi(self):
        """Vücut Kitle İndeksi hesaplama"""
        try:
            height_value = self.patient.patient_profile.height
            if not height_value:
                return None
            height_m = float(height_value) / 100
            weight = float(self.weight)
            return round(weight / (height_m ** 2), 1)
        except (AttributeError, ValueError, ZeroDivisionError):
            return None

    @property
    def waist_hip_ratio(self):
        """Bel-Kalça Oranı hesaplama"""
        if self.waist_circumference and self.hip_circumference:
            try:
                return round(float(self.waist_circumference) / float(self.hip_circumference), 2)
            except (ValueError, ZeroDivisionError):
                return None
        return None
