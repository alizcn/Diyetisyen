from django.conf import settings
from django.utils import translation

LANGUAGE_SESSION_KEY = getattr(translation, 'LANGUAGE_SESSION_KEY', 'django_language')


def _set_language_cookie(response, language_code):
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        language_code,
        max_age=getattr(settings, 'LANGUAGE_COOKIE_AGE', None),
        path=getattr(settings, 'LANGUAGE_COOKIE_PATH', '/'),
        domain=getattr(settings, 'LANGUAGE_COOKIE_DOMAIN', None),
        secure=getattr(settings, 'LANGUAGE_COOKIE_SECURE', False),
        httponly=getattr(settings, 'LANGUAGE_COOKIE_HTTPONLY', False),
        samesite=getattr(settings, 'LANGUAGE_COOKIE_SAMESITE', None),
    )


class UserLanguageMiddleware:
    """Kullanici girisliyse dil tercihine gore, degilse session/cookie'ye gore dili aktif eder."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.valid_languages = {code for code, _ in settings.LANGUAGES}

    def __call__(self, request):
        chosen_language = None
        session_language = request.session.get(LANGUAGE_SESSION_KEY)

        if request.user.is_authenticated:
            preferred = getattr(request.user, 'preferred_language', None)
            if preferred in self.valid_languages:
                chosen_language = preferred
                if session_language != preferred:
                    request.session[LANGUAGE_SESSION_KEY] = preferred

        if not chosen_language:
            if session_language in self.valid_languages:
                chosen_language = session_language
            else:
                cookie_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
                if cookie_lang in self.valid_languages:
                    chosen_language = cookie_lang

        if not chosen_language:
            chosen_language = settings.LANGUAGE_CODE

        translation.activate(chosen_language)
        request.LANGUAGE_CODE = chosen_language

        response = self.get_response(request)

        # Respect language changes made during the request cycle (e.g. language switch POST).
        cookie_language = request.session.get(LANGUAGE_SESSION_KEY)
        if cookie_language not in self.valid_languages:
            cookie_language = chosen_language

        response_cookie = response.cookies.get(settings.LANGUAGE_COOKIE_NAME)
        if request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME) != cookie_language and (
            response_cookie is None or response_cookie.value != cookie_language
        ):
            _set_language_cookie(response, cookie_language)
        return response
