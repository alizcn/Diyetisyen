from functools import wraps
from django.http import JsonResponse


def login_required_api(view_func):
    """Session-based authentication gerektirir"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Giriş yapmanız gerekli'}, status=401)
        return view_func(request, *args, **kwargs)

    return wrapper


def dietitian_required(view_func):
    """Sadece diyetisyenlerin erişebileceği view'lar için"""
    @wraps(view_func)
    @login_required_api
    def wrapper(request, *args, **kwargs):
        if request.user.user_type != 'dietitian':
            return JsonResponse({'error': 'Bu işlem için diyetisyen yetkisi gerekli'}, status=403)
        return view_func(request, *args, **kwargs)

    return wrapper


def patient_required(view_func):
    """Sadece hastaların erişebileceği view'lar için"""
    @wraps(view_func)
    @login_required_api
    def wrapper(request, *args, **kwargs):
        if request.user.user_type != 'patient':
            return JsonResponse({'error': 'Bu işlem için hasta yetkisi gerekli'}, status=403)
        return view_func(request, *args, **kwargs)

    return wrapper
