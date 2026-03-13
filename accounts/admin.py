from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DietitianProfile, PatientProfile


class DietitianProfileInline(admin.StackedInline):
    model = DietitianProfile
    can_delete = False
    verbose_name_plural = 'Diyetisyen Profili'


class PatientProfileInline(admin.StackedInline):
    model = PatientProfile
    can_delete = False
    verbose_name_plural = 'Hasta Profili'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Kişisel Bilgiler', {'fields': ('first_name', 'last_name', 'user_type')}),
        ('İzinler', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Önemli Tarihler', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'password1', 'password2'),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        inlines = []
        if obj.user_type == 'dietitian':
            inlines.append(DietitianProfileInline(self.model, self.admin_site))
        elif obj.user_type == 'patient':
            inlines.append(PatientProfileInline(self.model, self.admin_site))
        return inlines


@admin.register(DietitianProfile)
class DietitianProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience_years', 'city')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')
    list_filter = ('city',)


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dietitian', 'gender', 'current_weight', 'target_weight')
    search_fields = ('user__first_name', 'user__last_name')
    list_filter = ('gender', 'dietitian')
