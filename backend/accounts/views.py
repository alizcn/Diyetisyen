import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import User, DietitianProfile, PatientProfile
from .decorators import login_required_api


@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """Kullanıcı kaydı"""
    try:
        data = json.loads(request.body)

        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user_type = data.get('user_type', 'patient')

        if not all([email, password, first_name, last_name]):
            return JsonResponse({'error': 'Tüm alanlar zorunludur'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Bu email adresi zaten kullanılıyor'}, status=400)

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type
        )

        # Profil oluştur
        if user_type == 'dietitian':
            DietitianProfile.objects.create(user=user)
        else:
            PatientProfile.objects.create(user=user)

        # Session login
        auth_login(request, user)

        return JsonResponse({
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': user.user_type
            }
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Geçersiz JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """Kullanıcı girişi"""
    try:
        data = json.loads(request.body)

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({'error': 'Email ve şifre gereklidir'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Geçersiz email veya şifre'}, status=401)

        if not user.check_password(password):
            return JsonResponse({'error': 'Geçersiz email veya şifre'}, status=401)

        if not user.is_active:
            return JsonResponse({'error': 'Hesap aktif değil'}, status=401)

        # Session login
        auth_login(request, user)

        return JsonResponse({
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': user.user_type
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Geçersiz JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required_api
@require_http_methods(["GET"])
def me(request):
    """Mevcut kullanıcı bilgilerini döndürür"""
    user = request.user

    user_data = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'user_type': user.user_type,
        'date_joined': user.date_joined.isoformat()
    }

    # Profil bilgilerini ekle
    if user.user_type == 'dietitian':
        try:
            profile = user.dietitian_profile
            user_data['profile'] = {
                'bio': profile.bio,
                'specialization': profile.specialization,
                'experience_years': profile.experience_years,
                'phone': profile.phone,
                'city': profile.city,
                'photo': profile.photo.url if profile.photo else None
            }
        except DietitianProfile.DoesNotExist:
            DietitianProfile.objects.create(user=user)
            user_data['profile'] = {}
    else:
        try:
            profile = user.patient_profile
            user_data['profile'] = {
                'date_of_birth': profile.date_of_birth.isoformat() if profile.date_of_birth else None,
                'gender': profile.gender,
                'height': str(profile.height) if profile.height else None,
                'current_weight': str(profile.current_weight) if profile.current_weight else None,
                'target_weight': str(profile.target_weight) if profile.target_weight else None,
                'phone': profile.phone,
                'dietitian_id': profile.dietitian.id if profile.dietitian else None
            }
        except PatientProfile.DoesNotExist:
            PatientProfile.objects.create(user=user)
            user_data['profile'] = {}

    return JsonResponse(user_data)


@csrf_exempt
@login_required_api
@require_http_methods(["PUT"])
def update_profile(request):
    """Kullanıcı profili günceller"""
    try:
        data = json.loads(request.body)
        user = request.user

        # Temel bilgileri güncelle
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        user.save()

        # Profil bilgilerini güncelle
        if user.user_type == 'dietitian':
            profile, _ = DietitianProfile.objects.get_or_create(user=user)
            if 'bio' in data:
                profile.bio = data['bio']
            if 'specialization' in data:
                profile.specialization = data['specialization']
            if 'experience_years' in data:
                profile.experience_years = data['experience_years']
            if 'phone' in data:
                profile.phone = data['phone']
            if 'city' in data:
                profile.city = data['city']
            profile.save()
        else:
            profile, _ = PatientProfile.objects.get_or_create(user=user)
            if 'date_of_birth' in data:
                profile.date_of_birth = data['date_of_birth']
            if 'gender' in data:
                profile.gender = data['gender']
            if 'height' in data:
                profile.height = data['height']
            if 'current_weight' in data:
                profile.current_weight = data['current_weight']
            if 'target_weight' in data:
                profile.target_weight = data['target_weight']
            if 'phone' in data:
                profile.phone = data['phone']
            if 'dietitian_id' in data:
                if data['dietitian_id']:
                    dietitian = User.objects.get(id=data['dietitian_id'], user_type='dietitian')
                    profile.dietitian = dietitian
                else:
                    profile.dietitian = None
            profile.save()

        return JsonResponse({'message': 'Profil başarıyla güncellendi'})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Geçersiz JSON'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Diyetisyen bulunamadı'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def logout(request):
    """Kullanıcı çıkışı"""
    auth_logout(request)
    return JsonResponse({'message': 'Başarıyla çıkış yapıldı'})


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
                'photo': profile.photo.url if profile.photo else None
            })
        except DietitianProfile.DoesNotExist:
            continue

    return JsonResponse({'dietitians': data})
