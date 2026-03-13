from django.contrib import admin
from .models import DietPlan, Meal, Food, MealFood


class MealInline(admin.TabularInline):
    model = Meal
    extra = 1
    fields = ('meal_type', 'time', 'description', 'order')


@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'dietitian', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'dietitian', 'start_date')
    search_fields = ('title', 'patient__first_name', 'patient__last_name')
    date_hierarchy = 'start_date'
    inlines = [MealInline]

    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('title', 'description', 'patient', 'dietitian')
        }),
        ('Tarihler ve Hedefler', {
            'fields': ('start_date', 'end_date', 'daily_calories_target', 'is_active')
        }),
    )


class MealFoodInline(admin.TabularInline):
    model = MealFood
    extra = 1
    fields = ('food', 'quantity')


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('diet_plan', 'meal_type', 'time', 'order')
    list_filter = ('meal_type', 'diet_plan')
    inlines = [MealFoodInline]


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'portion_size', 'unit', 'calories', 'protein', 'carbs', 'fats')
    list_filter = ('unit', 'created_by')
    search_fields = ('name',)
    ordering = ('name',)

    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('name', 'portion_size', 'unit', 'created_by')
        }),
        ('Besin Değerleri', {
            'fields': ('calories', 'protein', 'carbs', 'fats', 'fiber')
        }),
    )


@admin.register(MealFood)
class MealFoodAdmin(admin.ModelAdmin):
    list_display = ('meal', 'food', 'quantity', 'total_calories')
    list_filter = ('meal__diet_plan',)

    def total_calories(self, obj):
        return f"{obj.total_calories:.1f} kcal"
    total_calories.short_description = 'Toplam Kalori'
