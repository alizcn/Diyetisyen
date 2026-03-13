from django.db import models
from django.conf import settings


class DietPlan(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='diet_plans',
        limit_choices_to={'user_type': 'patient'},
        verbose_name='Hasta'
    )
    dietitian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_diet_plans',
        limit_choices_to={'user_type': 'dietitian'},
        verbose_name='Diyetisyen'
    )
    title = models.CharField(max_length=200, verbose_name='Başlık')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    start_date = models.DateField(verbose_name='Başlangıç Tarihi')
    end_date = models.DateField(null=True, blank=True, verbose_name='Bitiş Tarihi')
    daily_calories_target = models.PositiveIntegerField(null=True, blank=True, verbose_name='Günlük Kalori Hedefi')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Diyet Planı'
        verbose_name_plural = 'Diyet Planları'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient.full_name} - {self.title}"


class Meal(models.Model):
    MEAL_TYPE_CHOICES = (
        ('breakfast', 'Kahvaltı'),
        ('morning_snack', 'Kuşluk'),
        ('lunch', 'Öğle Yemeği'),
        ('afternoon_snack', 'İkindi'),
        ('dinner', 'Akşam Yemeği'),
        ('evening_snack', 'Gece Atıştırması'),
    )

    diet_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE, related_name='meals', verbose_name='Diyet Planı')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, verbose_name='Öğün Tipi')
    time = models.TimeField(null=True, blank=True, verbose_name='Önerilen Saat')
    description = models.TextField(verbose_name='Açıklama')
    order = models.PositiveIntegerField(default=0, verbose_name='Sıra')

    class Meta:
        verbose_name = 'Öğün'
        verbose_name_plural = 'Öğünler'
        ordering = ['diet_plan', 'order']

    def __str__(self):
        return f"{self.diet_plan.title} - {self.get_meal_type_display()}"


class Food(models.Model):
    UNIT_CHOICES = (
        ('g', 'gram'),
        ('ml', 'mililitre'),
        ('adet', 'adet'),
        ('su_bardagi', 'su bardağı'),
        ('cay_bardagi', 'çay bardağı'),
        ('yemek_kasigi', 'yemek kaşığı'),
        ('cay_kasigi', 'çay kaşığı'),
        ('dilim', 'dilim'),
        ('porsiyon', 'porsiyon'),
    )

    name = models.CharField(max_length=200, verbose_name='Besin Adı')
    portion_size = models.DecimalField(max_digits=6, decimal_places=2, default=100, verbose_name='Porsiyon Miktarı')
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='g', verbose_name='Birim')
    calories = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Kalori')
    protein = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Protein (g)')
    carbs = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Karbonhidrat (g)')
    fats = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Yağ (g)')
    fiber = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Lif (g)')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'user_type': 'dietitian'},
        verbose_name='Oluşturan'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Besin'
        verbose_name_plural = 'Besinler'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.portion_size} {self.get_unit_display()})"


class MealFood(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='meal_foods', verbose_name='Öğün')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name='Besin')
    quantity = models.DecimalField(max_digits=6, decimal_places=2, default=1, verbose_name='Miktar')

    class Meta:
        verbose_name = 'Öğün Besini'
        verbose_name_plural = 'Öğün Besinleri'

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
