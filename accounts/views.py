from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import date

from .models import User, DietitianProfile, PatientProfile
from appointments.models import Appointment
from diets.models import DietPlan
from patients.models import Measurement


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
            user_type=form_data['user_type']
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

    # BMI calculation
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
        patient=user, status='scheduled', date__gte=date.today()
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

    patient_count = PatientProfile.objects.filter(dietitian=user).count()
    today_appointments = Appointment.objects.filter(dietitian=user, date=date.today()).exclude(status='cancelled')
    today_appointments_count = today_appointments.count()
    active_diet_count = DietPlan.objects.filter(dietitian=user, is_active=True).count()
    total_appointments = Appointment.objects.filter(dietitian=user).count()

    upcoming_appointments = Appointment.objects.filter(
        dietitian=user, date__gte=date.today(), status='scheduled'
    ).order_by('date', 'time')[:5]

    return render(request, 'dietitian/dashboard.html', {
        'active_page': 'dashboard',
        'patient_count': patient_count,
        'today_appointments_count': today_appointments_count,
        'active_diet_count': active_diet_count,
        'total_appointments': total_appointments,
        'upcoming_appointments': upcoming_appointments,
    })


@login_required
def dietitian_patients(request):
    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    patients = PatientProfile.objects.filter(dietitian=user).select_related('user')

    return render(request, 'dietitian/patients.html', {
        'active_page': 'patients',
        'patients': patients,
    })


@login_required
def dietitian_diets(request):
    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    diet_plans = DietPlan.objects.filter(dietitian=user).select_related('patient').order_by('-created_at')

    return render(request, 'dietitian/diets.html', {
        'active_page': 'diets',
        'diet_plans': diet_plans,
    })


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
