from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email adresi zorunludur')
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
        ('dietitian', 'Diyetisyen'),
        ('patient', 'Hasta'),
    )

    email = models.EmailField(unique=True, verbose_name='E-posta')
    first_name = models.CharField(max_length=50, verbose_name='Ad')
    last_name = models.CharField(max_length=50, verbose_name='Soyad')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, verbose_name='Kullanıcı Tipi')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class DietitianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dietitian_profile')
    bio = models.TextField(blank=True, verbose_name='Hakkında')
    specialization = models.CharField(max_length=200, blank=True, verbose_name='Uzmanlık Alanı')
    experience_years = models.PositiveIntegerField(default=0, verbose_name='Deneyim (Yıl)')
    photo = models.ImageField(upload_to='dietitians/', blank=True, null=True, verbose_name='Fotoğraf')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')
    address = models.TextField(blank=True, verbose_name='Adres')
    city = models.CharField(max_length=100, blank=True, verbose_name='Şehir')
    license_number = models.CharField(max_length=50, blank=True, verbose_name='Diploma No')

    class Meta:
        verbose_name = 'Diyetisyen Profili'
        verbose_name_plural = 'Diyetisyen Profilleri'

    def __str__(self):
        return f"{self.user.full_name} - Diyetisyen"


class PatientProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Erkek'),
        ('F', 'Kadın'),
        ('O', 'Diğer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    dietitian = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients',
        limit_choices_to={'user_type': 'dietitian'},
        verbose_name='Diyetisyen'
    )
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='Cinsiyet')
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Boy (cm)')
    current_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Mevcut Kilo (kg)')
    target_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Hedef Kilo (kg)')
    medical_conditions = models.TextField(blank=True, verbose_name='Tıbbi Durumlar/Notlar')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')

    class Meta:
        verbose_name = 'Hasta Profili'
        verbose_name_plural = 'Hasta Profilleri'

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
