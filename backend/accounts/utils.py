import jwt
import datetime
from functools import wraps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()


def generate_jwt_token(user):
    """JWT token oluşturur"""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'user_type': user.user_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_jwt_token(token):
    """JWT token'ı decode eder"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_user_from_token(token):
    """Token'dan user objesini getirir"""
    payload = decode_jwt_token(token)
    if payload:
        try:
            user = User.objects.get(id=payload['user_id'])
            return user
        except User.DoesNotExist:
            return None
    return None


def jwt_required(view_func):
    """JWT authentication decorator"""
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'No token provided'}, status=401)

        token = auth_header.split(' ')[1]

        # Decode token and get user
        user = get_user_from_token(token)

        if not user:
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)

        # Attach user to request
        request.user = user

        return view_func(request, *args, **kwargs)

    return wrapped_view
