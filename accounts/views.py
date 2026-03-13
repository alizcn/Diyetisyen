from decimal import Decimal, InvalidOperation
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import DietitianProfile, PatientProfile, User
from appointments.models import Appointment
from diets.models import DietPlan, Food


def _parse_decimal(value):
    value = (value or '').strip()
    if not value:
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return 'invalid'


def _parse_int(value):
    value = (value or '').strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return 'invalid'


def _parse_date(value):
    value = (value or '').strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return 'invalid'


# ==================== PUBLIC / AUTH ====================

def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'dietitian':
            return redirect('dietitian_dashboard')
        return redirect('patient_dashboard')
    return render(request, 'home.html')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'dietitian':
            return redirect('dietitian_dashboard')
        return redirect('patient_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            return render(request, 'accounts/login.html', {'error': 'Email ve şifre gereklidir', 'email': email})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'accounts/login.html', {'error': 'Geçersiz email veya şifre', 'email': email})

        if not user.check_password(password):
            return render(request, 'accounts/login.html', {'error': 'Geçersiz email veya şifre', 'email': email})

        if not user.is_active:
            return render(request, 'accounts/login.html', {'error': 'Hesap aktif değil', 'email': email})

        auth_login(request, user)

        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url:
            return redirect(next_url)

        if user.user_type == 'dietitian':
            return redirect('dietitian_dashboard')
        return redirect('patient_dashboard')

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form_data = {
            'email': request.POST.get('email', '').strip(),
            'first_name': request.POST.get('first_name', '').strip(),
            'last_name': request.POST.get('last_name', '').strip(),
            'user_type': request.POST.get('user_type', 'patient'),
        }
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([form_data['email'], form_data['first_name'], form_data['last_name'], password]):
            return render(request, 'accounts/register.html', {'error': 'Tüm alanlar zorunludur', 'form_data': form_data})

        if password != confirm_password:
            return render(request, 'accounts/register.html', {'error': 'Şifreler eşleşmiyor', 'form_data': form_data})

        if len(password) < 6:
            return render(request, 'accounts/register.html', {'error': 'Şifre en az 6 karakter olmalıdır', 'form_data': form_data})

        if User.objects.filter(email=form_data['email']).exists():
            return render(request, 'accounts/register.html', {'error': 'Bu email adresi zaten kullanılıyor', 'form_data': form_data})

        user = User.objects.create_user(
            email=form_data['email'],
            password=password,
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            user_type=form_data['user_type'],
        )

        if form_data['user_type'] == 'dietitian':
            DietitianProfile.objects.create(user=user)
        else:
            PatientProfile.objects.create(user=user)

        auth_login(request, user)

        if user.user_type == 'dietitian':
            return redirect('dietitian_dashboard')
        return redirect('patient_dashboard')

    return render(request, 'accounts/register.html')


@require_http_methods(["POST"])
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'Başarıyla çıkış yapıldı')
    return redirect('login')


# ==================== PATIENT VIEWS ====================

@login_required
def patient_dashboard(request):
    user = request.user
    if user.user_type != 'patient':
        return redirect('dietitian_dashboard')

    profile, _ = PatientProfile.objects.get_or_create(user=user)

    bmi = None
    bmi_label = None
    if profile.height and profile.current_weight:
        height_m = float(profile.height) / 100
        bmi = round(float(profile.current_weight) / (height_m ** 2), 1)
        if bmi < 18.5:
            bmi_label = 'Zayıf'
        elif bmi < 25:
            bmi_label = 'Normal'
        elif bmi < 30:
            bmi_label = 'Hafif Kilolu'
        else:
            bmi_label = 'Obez'

    next_appointment = Appointment.objects.filter(
        patient=user,
        status='scheduled',
        date__gte=date.today(),
    ).order_by('date', 'time').first()

    active_diet = DietPlan.objects.filter(patient=user, is_active=True).first()

    return render(request, 'accounts/patient_dashboard.html', {
        'active_page': 'dashboard',
        'profile': profile,
        'bmi': bmi,
        'bmi_label': bmi_label,
        'next_appointment': next_appointment,
        'active_diet': active_diet,
    })


@login_required
def patient_diet_plan(request):
    user = request.user
    if user.user_type != 'patient':
        return redirect('dietitian_dashboard')

    diet_plan = DietPlan.objects.filter(patient=user, is_active=True).first()
    meals = []
    if diet_plan:
        meals = diet_plan.meals.all().prefetch_related('meal_foods__food').order_by('order')

    return render(request, 'accounts/patient_diet_plan.html', {
        'active_page': 'diet_plan',
        'diet_plan': diet_plan,
        'meals': meals,
    })


# ==================== DIETITIAN VIEWS ====================

@login_required
def dietitian_dashboard(request):
    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    patient_count = PatientProfile.objects.filter(dietitian=user).count()
    today_appointments_count = Appointment.objects.filter(
        dietitian=user,
        date=today,
    ).exclude(status='cancelled').count()

    weekly_appointments_qs = Appointment.objects.filter(
        dietitian=user,
        date__gte=week_start,
        date__lte=week_end,
    ).exclude(status='cancelled')
    weekly_appointments_count = weekly_appointments_qs.count()

    active_diet_count = DietPlan.objects.filter(dietitian=user, is_active=True).count()
    total_appointments = Appointment.objects.filter(dietitian=user).count()

    upcoming_appointments = Appointment.objects.filter(
        dietitian=user,
        date__gte=week_start,
        date__lte=week_end,
        status__in=['scheduled', 'confirmed'],
    ).order_by('date', 'time')

    return render(request, 'dietitian/dashboard.html', {
        'active_page': 'dashboard',
        'patient_count': patient_count,
        'today_appointments_count': today_appointments_count,
        'weekly_appointments_count': weekly_appointments_count,
        'active_diet_count': active_diet_count,
        'total_appointments': total_appointments,
        'upcoming_appointments': upcoming_appointments,
        'week_start': week_start,
        'week_end': week_end,
    })


@login_required
def dietitian_profile_edit(request):
    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    profile, _ = DietitianProfile.objects.get_or_create(user=user)

    form_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': profile.phone,
        'city': profile.city,
        'address': profile.address,
        'specialization': profile.specialization,
        'experience_years': profile.experience_years,
        'license_number': profile.license_number,
        'bio': profile.bio,
    }

    if request.method == 'POST':
        form_data = {
            'first_name': request.POST.get('first_name', '').strip(),
            'last_name': request.POST.get('last_name', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
            'city': request.POST.get('city', '').strip(),
            'address': request.POST.get('address', '').strip(),
            'specialization': request.POST.get('specialization', '').strip(),
            'experience_years': request.POST.get('experience_years', '').strip(),
            'license_number': request.POST.get('license_number', '').strip(),
            'bio': request.POST.get('bio', '').strip(),
        }

        if not all([form_data['first_name'], form_data['last_name'], form_data['email']]):
            return render(request, 'dietitian/profile_edit.html', {
                'active_page': 'profile',
                'profile': profile,
                'form_data': form_data,
                'error': 'Ad, soyad ve e-posta zorunludur.',
            })

        if User.objects.filter(email=form_data['email']).exclude(id=user.id).exists():
            return render(request, 'dietitian/profile_edit.html', {
                'active_page': 'profile',
                'profile': profile,
                'form_data': form_data,
                'error': 'Bu e-posta başka bir kullanıcı tarafından kullanılıyor.',
            })

        experience_years = _parse_int(form_data['experience_years'])
        if experience_years == 'invalid' or (experience_years is not None and experience_years < 0):
            return render(request, 'dietitian/profile_edit.html', {
                'active_page': 'profile',
                'profile': profile,
                'form_data': form_data,
                'error': 'Deneyim yılı geçerli bir sayı olmalıdır.',
            })

        user.first_name = form_data['first_name']
        user.last_name = form_data['last_name']
        user.email = form_data['email']
        user.save()

        profile.phone = form_data['phone']
        profile.city = form_data['city']
        profile.address = form_data['address']
        profile.specialization = form_data['specialization']
        profile.experience_years = experience_years or 0
        profile.license_number = form_data['license_number']
        profile.bio = form_data['bio']
        profile.save()

        messages.success(request, 'Profil bilgileriniz güncellendi.')
        return redirect('dietitian_profile_edit')

    return render(request, 'dietitian/profile_edit.html', {
        'active_page': 'profile',
        'profile': profile,
        'form_data': form_data,
    })


@login_required
def dietitian_patients(request):
    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    patients = PatientProfile.objects.filter(dietitian=user).select_related('user').order_by('user__first_name', 'user__last_name')

    return render(request, 'dietitian/patients.html', {
        'active_page': 'patients',
        'patients': patients,
    })


@login_required
def dietitian_patient_edit(request, patient_id):
    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    patient_profile = get_object_or_404(
        PatientProfile.objects.select_related('user'),
        id=patient_id,
        dietitian=user,
    )
    patient_user = patient_profile.user

    form_data = {
        'first_name': patient_user.first_name,
        'last_name': patient_user.last_name,
        'email': patient_user.email,
        'phone': patient_profile.phone,
        'date_of_birth': patient_profile.date_of_birth.isoformat() if patient_profile.date_of_birth else '',
        'gender': patient_profile.gender,
        'height': patient_profile.height if patient_profile.height is not None else '',
        'current_weight': patient_profile.current_weight if patient_profile.current_weight is not None else '',
        'target_weight': patient_profile.target_weight if patient_profile.target_weight is not None else '',
        'medical_conditions': patient_profile.medical_conditions,
    }

    if request.method == 'POST':
        form_data = {
            'first_name': request.POST.get('first_name', '').strip(),
            'last_name': request.POST.get('last_name', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
            'date_of_birth': request.POST.get('date_of_birth', '').strip(),
            'gender': request.POST.get('gender', '').strip(),
            'height': request.POST.get('height', '').strip(),
            'current_weight': request.POST.get('current_weight', '').strip(),
            'target_weight': request.POST.get('target_weight', '').strip(),
            'medical_conditions': request.POST.get('medical_conditions', '').strip(),
        }

        if not all([form_data['first_name'], form_data['last_name'], form_data['email']]):
            return render(request, 'dietitian/patient_edit.html', {
                'active_page': 'patients',
                'patient_profile': patient_profile,
                'form_data': form_data,
                'error': 'Ad, soyad ve e-posta zorunludur.',
            })

        if User.objects.filter(email=form_data['email']).exclude(id=patient_user.id).exists():
            return render(request, 'dietitian/patient_edit.html', {
                'active_page': 'patients',
                'patient_profile': patient_profile,
                'form_data': form_data,
                'error': 'Bu e-posta başka bir kullanıcı tarafından kullanılıyor.',
            })

        date_of_birth = _parse_date(form_data['date_of_birth'])
        if date_of_birth == 'invalid':
            return render(request, 'dietitian/patient_edit.html', {
                'active_page': 'patients',
                'patient_profile': patient_profile,
                'form_data': form_data,
                'error': 'Doğum tarihi formatı geçersiz.',
            })

        height = _parse_decimal(form_data['height'])
        current_weight = _parse_decimal(form_data['current_weight'])
        target_weight = _parse_decimal(form_data['target_weight'])

        if 'invalid' in (height, current_weight, target_weight):
            return render(request, 'dietitian/patient_edit.html', {
                'active_page': 'patients',
                'patient_profile': patient_profile,
                'form_data': form_data,
                'error': 'Boy ve kilo alanları sayısal olmalıdır.',
            })

        if form_data['gender'] and form_data['gender'] not in {'M', 'F', 'O'}:
            return render(request, 'dietitian/patient_edit.html', {
                'active_page': 'patients',
                'patient_profile': patient_profile,
                'form_data': form_data,
                'error': 'Cinsiyet seçimi geçersiz.',
            })

        patient_user.first_name = form_data['first_name']
        patient_user.last_name = form_data['last_name']
        patient_user.email = form_data['email']
        patient_user.save()

        patient_profile.phone = form_data['phone']
        patient_profile.date_of_birth = date_of_birth
        patient_profile.gender = form_data['gender']
        patient_profile.height = height
        patient_profile.current_weight = current_weight
        patient_profile.target_weight = target_weight
        patient_profile.medical_conditions = form_data['medical_conditions']
        patient_profile.save()

        messages.success(request, 'Hasta bilgileri güncellendi.')
        return redirect('dietitian_patients')

    return render(request, 'dietitian/patient_edit.html', {
        'active_page': 'patients',
        'patient_profile': patient_profile,
        'form_data': form_data,
    })


@login_required
def dietitian_patient_delete(request, patient_id):
    if request.method != 'POST':
        return redirect('dietitian_patients')

    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    patient_profile = get_object_or_404(PatientProfile.objects.select_related('user'), id=patient_id, dietitian=user)
    patient_name = patient_profile.user.full_name
    patient_profile.user.delete()

    messages.success(request, f'{patient_name} adlı hasta silindi.')
    return redirect('dietitian_patients')


@login_required
def dietitian_diets(request):
    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    patient_profiles = PatientProfile.objects.filter(dietitian=user).select_related('user').order_by('user__first_name', 'user__last_name')
    selected_patient_id = request.GET.get('patient', '').strip()

    diet_plans = DietPlan.objects.filter(dietitian=user).select_related('patient').order_by('-created_at')

    selected_patient = None
    if selected_patient_id.isdigit():
        selected_patient = patient_profiles.filter(user_id=int(selected_patient_id)).first()
        if selected_patient:
            diet_plans = diet_plans.filter(patient_id=selected_patient.user_id)

    foods = Food.objects.filter(Q(created_by=user) | Q(created_by__isnull=True)).order_by('name')

    return render(request, 'dietitian/diets.html', {
        'active_page': 'diets',
        'diet_plans': diet_plans,
        'foods': foods,
        'patient_profiles': patient_profiles,
        'selected_patient': selected_patient,
        'selected_patient_id': selected_patient.user_id if selected_patient else None,
        'unit_choices': Food.UNIT_CHOICES,
    })


@login_required
def dietitian_diet_edit(request, plan_id):
    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    diet_plan = get_object_or_404(DietPlan, id=plan_id, dietitian=user)
    patient_profiles = PatientProfile.objects.filter(dietitian=user).select_related('user').order_by('user__first_name', 'user__last_name')

    form_data = {
        'patient_id': str(diet_plan.patient_id),
        'title': diet_plan.title,
        'description': diet_plan.description,
        'start_date': diet_plan.start_date.isoformat() if diet_plan.start_date else '',
        'end_date': diet_plan.end_date.isoformat() if diet_plan.end_date else '',
        'daily_calories_target': diet_plan.daily_calories_target if diet_plan.daily_calories_target is not None else '',
        'is_active': diet_plan.is_active,
    }

    if request.method == 'POST':
        form_data = {
            'patient_id': request.POST.get('patient_id', '').strip(),
            'title': request.POST.get('title', '').strip(),
            'description': request.POST.get('description', '').strip(),
            'start_date': request.POST.get('start_date', '').strip(),
            'end_date': request.POST.get('end_date', '').strip(),
            'daily_calories_target': request.POST.get('daily_calories_target', '').strip(),
            'is_active': request.POST.get('is_active') == 'on',
        }

        if not all([form_data['patient_id'], form_data['title'], form_data['start_date']]):
            return render(request, 'dietitian/diet_edit.html', {
                'active_page': 'diets',
                'diet_plan': diet_plan,
                'patient_profiles': patient_profiles,
                'form_data': form_data,
                'error': 'Hasta, başlık ve başlangıç tarihi zorunludur.',
            })

        if not form_data['patient_id'].isdigit() or not patient_profiles.filter(user_id=int(form_data['patient_id'])).exists():
            return render(request, 'dietitian/diet_edit.html', {
                'active_page': 'diets',
                'diet_plan': diet_plan,
                'patient_profiles': patient_profiles,
                'form_data': form_data,
                'error': 'Geçerli bir hasta seçiniz.',
            })

        start_date_value = _parse_date(form_data['start_date'])
        end_date_value = _parse_date(form_data['end_date'])

        if start_date_value == 'invalid' or end_date_value == 'invalid':
            return render(request, 'dietitian/diet_edit.html', {
                'active_page': 'diets',
                'diet_plan': diet_plan,
                'patient_profiles': patient_profiles,
                'form_data': form_data,
                'error': 'Tarih formatı geçersiz.',
            })

        if end_date_value and start_date_value and end_date_value < start_date_value:
            return render(request, 'dietitian/diet_edit.html', {
                'active_page': 'diets',
                'diet_plan': diet_plan,
                'patient_profiles': patient_profiles,
                'form_data': form_data,
                'error': 'Bitiş tarihi başlangıç tarihinden önce olamaz.',
            })

        calories = _parse_int(form_data['daily_calories_target'])
        if calories == 'invalid' or (calories is not None and calories < 0):
            return render(request, 'dietitian/diet_edit.html', {
                'active_page': 'diets',
                'diet_plan': diet_plan,
                'patient_profiles': patient_profiles,
                'form_data': form_data,
                'error': 'Kalori hedefi pozitif bir sayı olmalıdır.',
            })

        diet_plan.patient_id = int(form_data['patient_id'])
        diet_plan.title = form_data['title']
        diet_plan.description = form_data['description']
        diet_plan.start_date = start_date_value
        diet_plan.end_date = end_date_value
        diet_plan.daily_calories_target = calories
        diet_plan.is_active = form_data['is_active']
        diet_plan.save()

        messages.success(request, 'Diyet planı güncellendi.')
        return redirect('dietitian_diets')

    return render(request, 'dietitian/diet_edit.html', {
        'active_page': 'diets',
        'diet_plan': diet_plan,
        'patient_profiles': patient_profiles,
        'form_data': form_data,
    })


@login_required
def dietitian_diet_delete(request, plan_id):
    if request.method != 'POST':
        return redirect('dietitian_diets')

    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    diet_plan = get_object_or_404(DietPlan, id=plan_id, dietitian=user)
    title = diet_plan.title
    diet_plan.delete()

    messages.success(request, f'"{title}" diyet planı silindi.')
    return redirect('dietitian_diets')


@login_required
def dietitian_food_create(request):
    if request.method != 'POST':
        return redirect('dietitian_diets')

    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    form_data = {
        'name': request.POST.get('name', '').strip(),
        'portion_size': request.POST.get('portion_size', '').strip(),
        'unit': request.POST.get('unit', '').strip(),
        'calories': request.POST.get('calories', '').strip(),
        'protein': request.POST.get('protein', '').strip(),
        'carbs': request.POST.get('carbs', '').strip(),
        'fats': request.POST.get('fats', '').strip(),
        'fiber': request.POST.get('fiber', '').strip(),
    }

    if not form_data['name'] or not form_data['calories']:
        messages.error(request, 'Besin adı ve kalori zorunludur.')
        return redirect('dietitian_diets')

    if form_data['unit'] not in dict(Food.UNIT_CHOICES):
        messages.error(request, 'Besin birimi geçersiz.')
        return redirect('dietitian_diets')

    portion_size = _parse_decimal(form_data['portion_size'])
    calories = _parse_decimal(form_data['calories'])
    protein = _parse_decimal(form_data['protein'])
    carbs = _parse_decimal(form_data['carbs'])
    fats = _parse_decimal(form_data['fats'])
    fiber = _parse_decimal(form_data['fiber'])

    if 'invalid' in (portion_size, calories, protein, carbs, fats, fiber):
        messages.error(request, 'Besin değerleri sayısal olmalıdır.')
        return redirect('dietitian_diets')

    Food.objects.create(
        name=form_data['name'],
        portion_size=portion_size if portion_size is not None else Decimal('100'),
        unit=form_data['unit'],
        calories=calories,
        protein=protein if protein is not None else Decimal('0'),
        carbs=carbs if carbs is not None else Decimal('0'),
        fats=fats if fats is not None else Decimal('0'),
        fiber=fiber if fiber is not None else Decimal('0'),
        created_by=user,
    )

    messages.success(request, 'Yeni besin kaydı eklendi.')
    return redirect('dietitian_diets')


@login_required
def dietitian_food_edit(request, food_id):
    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    food = get_object_or_404(Food.objects.filter(Q(created_by=user) | Q(created_by__isnull=True)), id=food_id)

    form_data = {
        'name': food.name,
        'portion_size': food.portion_size,
        'unit': food.unit,
        'calories': food.calories,
        'protein': food.protein,
        'carbs': food.carbs,
        'fats': food.fats,
        'fiber': food.fiber,
    }

    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name', '').strip(),
            'portion_size': request.POST.get('portion_size', '').strip(),
            'unit': request.POST.get('unit', '').strip(),
            'calories': request.POST.get('calories', '').strip(),
            'protein': request.POST.get('protein', '').strip(),
            'carbs': request.POST.get('carbs', '').strip(),
            'fats': request.POST.get('fats', '').strip(),
            'fiber': request.POST.get('fiber', '').strip(),
        }

        if not form_data['name'] or not form_data['calories']:
            return render(request, 'dietitian/food_edit.html', {
                'active_page': 'diets',
                'food': food,
                'form_data': form_data,
                'unit_choices': Food.UNIT_CHOICES,
                'error': 'Besin adı ve kalori zorunludur.',
            })

        if form_data['unit'] not in dict(Food.UNIT_CHOICES):
            return render(request, 'dietitian/food_edit.html', {
                'active_page': 'diets',
                'food': food,
                'form_data': form_data,
                'unit_choices': Food.UNIT_CHOICES,
                'error': 'Besin birimi geçersiz.',
            })

        portion_size = _parse_decimal(form_data['portion_size'])
        calories = _parse_decimal(form_data['calories'])
        protein = _parse_decimal(form_data['protein'])
        carbs = _parse_decimal(form_data['carbs'])
        fats = _parse_decimal(form_data['fats'])
        fiber = _parse_decimal(form_data['fiber'])

        if 'invalid' in (portion_size, calories, protein, carbs, fats, fiber):
            return render(request, 'dietitian/food_edit.html', {
                'active_page': 'diets',
                'food': food,
                'form_data': form_data,
                'unit_choices': Food.UNIT_CHOICES,
                'error': 'Besin değerleri sayısal olmalıdır.',
            })

        food.name = form_data['name']
        food.portion_size = portion_size if portion_size is not None else Decimal('100')
        food.unit = form_data['unit']
        food.calories = calories
        food.protein = protein if protein is not None else Decimal('0')
        food.carbs = carbs if carbs is not None else Decimal('0')
        food.fats = fats if fats is not None else Decimal('0')
        food.fiber = fiber if fiber is not None else Decimal('0')
        if food.created_by is None:
            food.created_by = user
        food.save()

        messages.success(request, 'Besin kaydı güncellendi.')
        return redirect('dietitian_diets')

    return render(request, 'dietitian/food_edit.html', {
        'active_page': 'diets',
        'food': food,
        'form_data': form_data,
        'unit_choices': Food.UNIT_CHOICES,
    })


@login_required
def dietitian_food_delete(request, food_id):
    if request.method != 'POST':
        return redirect('dietitian_diets')

    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    food = get_object_or_404(Food.objects.filter(Q(created_by=user) | Q(created_by__isnull=True)), id=food_id)
    name = food.name
    food.delete()

    messages.success(request, f'"{name}" besin kaydı silindi.')
    return redirect('dietitian_diets')


# ==================== API VIEWS (kept for backward compat) ====================

@require_http_methods(["GET"])
def list_dietitians(request):
    """Tüm diyetisyenleri listeler (public endpoint)"""
    dietitians = User.objects.filter(user_type='dietitian', is_active=True)
    data = []
    for dietitian in dietitians:
        try:
            profile = dietitian.dietitian_profile
            data.append({
                'id': dietitian.id,
                'first_name': dietitian.first_name,
                'last_name': dietitian.last_name,
                'full_name': dietitian.full_name,
                'bio': profile.bio,
                'specialization': profile.specialization,
                'experience_years': profile.experience_years,
                'city': profile.city,
            })
        except DietitianProfile.DoesNotExist:
            continue
    return JsonResponse({'dietitians': data})
