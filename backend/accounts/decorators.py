from functools import wraps
from django.http import JsonResponse
from .utils import get_user_from_token


def jwt_required(view_func):
    """JWT authentication gerektirir"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return JsonResponse({'error': 'Authorization header gerekli'}, status=401)

        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                return JsonResponse({'error': 'Bearer token gerekli'}, status=401)
        except ValueError:
            return JsonResponse({'error': 'Geçersiz authorization header formatı'}, status=401)

        user = get_user_from_token(token)
        if not user:
            return JsonResponse({'error': 'Geçersiz veya süresi dolmuş token'}, status=401)

        request.user = user
        return view_func(request, *args, **kwargs)

    return wrapper


def dietitian_required(view_func):
    """Sadece diyetisyenlerin erişebileceği view'lar için"""
    @wraps(view_func)
    @jwt_required
    def wrapper(request, *args, **kwargs):
        if request.user.user_type != 'dietitian':
            return JsonResponse({'error': 'Bu işlem için diyetisyen yetkisi gerekli'}, status=403)
        return view_func(request, *args, **kwargs)

    return wrapper


def patient_required(view_func):
    """Sadece hastaların erişebileceği view'lar için"""
    @wraps(view_func)
    @jwt_required
    def wrapper(request, *args, **kwargs):
        if request.user.user_type != 'patient':
            return JsonResponse({'error': 'Bu işlem için hasta yetkisi gerekli'}, status=403)
        return view_func(request, *args, **kwargs)

    return wrapper
