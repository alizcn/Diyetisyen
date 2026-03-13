from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class DietPlan(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='diet_plans',
        limit_choices_to={'user_type': 'patient'},
        verbose_name=_('Hasta')
    )
    dietitian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_diet_plans',
        limit_choices_to={'user_type': 'dietitian'},
        verbose_name=_('Diyetisyen')
    )
    title = models.CharField(max_length=200, verbose_name=_('Başlık'))
    description = models.TextField(blank=True, verbose_name=_('Açıklama'))
    start_date = models.DateField(verbose_name=_('Başlangıç Tarihi'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_('Bitiş Tarihi'))
    daily_calories_target = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Günlük Kalori Hedefi'))
    is_active = models.BooleanField(default=True, verbose_name=_('Aktif'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Diyet Planı')
        verbose_name_plural = _('Diyet Planları')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient.full_name} - {self.title}"


class Meal(models.Model):
    MEAL_TYPE_CHOICES = (
        ('breakfast', _('Kahvaltı')),
        ('morning_snack', _('Kuşluk')),
        ('lunch', _('Öğle Yemeği')),
        ('afternoon_snack', _('İkindi')),
        ('dinner', _('Akşam Yemeği')),
        ('evening_snack', _('Gece Atıştırması')),
    )

    diet_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE, related_name='meals', verbose_name=_('Diyet Planı'))
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, verbose_name=_('Öğün Tipi'))
    time = models.TimeField(null=True, blank=True, verbose_name=_('Önerilen Saat'))
    description = models.TextField(verbose_name=_('Açıklama'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Sıra'))

    class Meta:
        verbose_name = _('Öğün')
        verbose_name_plural = _('Öğünler')
        ordering = ['diet_plan', 'order']

    def __str__(self):
        return f"{self.diet_plan.title} - {self.get_meal_type_display()}"


class Food(models.Model):
    UNIT_CHOICES = (
        ('g', _('gram')),
        ('ml', _('mililitre')),
        ('adet', _('adet')),
        ('su_bardagi', _('su bardağı')),
        ('cay_bardagi', _('çay bardağı')),
        ('yemek_kasigi', _('yemek kaşığı')),
        ('cay_kasigi', _('çay kaşığı')),
        ('dilim', _('dilim')),
        ('porsiyon', _('porsiyon')),
    )

    name = models.CharField(max_length=200, verbose_name=_('Besin Adı'))
    portion_size = models.DecimalField(max_digits=6, decimal_places=2, default=100, verbose_name=_('Porsiyon Miktarı'))
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='g', verbose_name=_('Birim'))
    calories = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('Kalori'))
    protein = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name=_('Protein (g)'))
    carbs = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name=_('Karbonhidrat (g)'))
    fats = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name=_('Yağ (g)'))
    fiber = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name=_('Lif (g)'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'user_type': 'dietitian'},
        verbose_name=_('Oluşturan')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Besin')
        verbose_name_plural = _('Besinler')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.portion_size} {self.get_unit_display()})"


class MealFood(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='meal_foods', verbose_name=_('Öğün'))
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name=_('Besin'))
    quantity = models.DecimalField(max_digits=6, decimal_places=2, default=1, verbose_name=_('Miktar'))

    class Meta:
        verbose_name = _('Öğün Besini')
        verbose_name_plural = _('Öğün Besinleri')

    def __str__(self):
        return f"{self.meal} - {self.food.name} ({self.quantity})"

    @property
    def total_calories(self):
        return float(self.food.calories) * float(self.quantity)

    @property
    def total_protein(self):
        return float(self.food.protein) * float(self.quantity)

    @property
    def total_carbs(self):
        return float(self.food.carbs) * float(self.quantity)

    @property
    def total_fats(self):
        return float(self.food.fats) * float(self.quantity)
