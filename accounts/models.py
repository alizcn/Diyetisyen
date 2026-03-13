from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email adresi zorunludur'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'dietitian')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('dietitian', _('Diyetisyen')),
        ('patient', _('Hasta')),
    )
    LANGUAGE_CHOICES = (
        ('tr', _('Türkçe')),
        ('en', _('English')),
    )

    email = models.EmailField(unique=True, verbose_name=_('E-posta'))
    first_name = models.CharField(max_length=50, verbose_name=_('Ad'))
    last_name = models.CharField(max_length=50, verbose_name=_('Soyad'))
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, verbose_name=_('Kullanıcı Tipi'))
    preferred_language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='tr', verbose_name=_('Tercih Edilen Dil'))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('Kullanıcı')
        verbose_name_plural = _('Kullanıcılar')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class DietitianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dietitian_profile')
    bio = models.TextField(blank=True, verbose_name=_('Hakkında'))
    specialization = models.CharField(max_length=200, blank=True, verbose_name=_('Uzmanlık Alanı'))
    experience_years = models.PositiveIntegerField(default=0, verbose_name=_('Deneyim (Yıl)'))
    photo = models.ImageField(upload_to='dietitians/', blank=True, null=True, verbose_name=_('Fotoğraf'))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_('Telefon'))
    address = models.TextField(blank=True, verbose_name=_('Adres'))
    city = models.CharField(max_length=100, blank=True, verbose_name=_('Şehir'))
    license_number = models.CharField(max_length=50, blank=True, verbose_name=_('Diploma No'))

    class Meta:
        verbose_name = _('Diyetisyen Profili')
        verbose_name_plural = _('Diyetisyen Profilleri')

    def __str__(self):
        return f"{self.user.full_name} - Diyetisyen"


class PatientProfile(models.Model):
    GENDER_CHOICES = (
        ('M', _('Erkek')),
        ('F', _('Kadın')),
        ('O', _('Diğer')),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    dietitian = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients',
        limit_choices_to={'user_type': 'dietitian'},
        verbose_name=_('Diyetisyen')
    )
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Doğum Tarihi'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name=_('Cinsiyet'))
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Boy (cm)'))
    current_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Mevcut Kilo (kg)'))
    target_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Hedef Kilo (kg)'))
    medical_conditions = models.TextField(blank=True, verbose_name=_('Tıbbi Durumlar/Notlar'))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_('Telefon'))

    class Meta:
        verbose_name = _('Hasta Profili')
        verbose_name_plural = _('Hasta Profilleri')

    def __str__(self):
        return f"{self.user.full_name} - Hasta"

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
