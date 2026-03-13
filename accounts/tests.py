from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from .models import User

LANGUAGE_SESSION_KEY = getattr(translation, 'LANGUAGE_SESSION_KEY', 'django_language')


class LanguagePreferenceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='patient@example.com',
            password='strong-password',
            first_name='Test',
            last_name='Patient',
            user_type='patient',
            preferred_language='tr',
        )

    def test_set_language_preference_persists_for_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('set_language_preference'),
            {'language': 'en', 'next': '/'},
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.preferred_language, 'en')
        self.assertEqual(self.client.session.get(LANGUAGE_SESSION_KEY), 'en')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, 'en')

    def test_set_language_preference_for_anonymous_updates_session(self):
        response = self.client.post(
            reverse('set_language_preference'),
            {'language': 'en', 'next': '/'},
        )

        self.assertEqual(self.client.session.get(LANGUAGE_SESSION_KEY), 'en')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, 'en')

    def test_invalid_language_falls_back_to_default(self):
        response = self.client.post(
            reverse('set_language_preference'),
            {'language': 'xx', 'next': '/'},
        )

        self.assertEqual(self.client.session.get(LANGUAGE_SESSION_KEY), settings.LANGUAGE_CODE)
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, settings.LANGUAGE_CODE)

    def test_user_preference_overrides_session_and_cookie(self):
        self.user.preferred_language = 'en'
        self.user.save(update_fields=['preferred_language'])
        self.client.force_login(self.user)

        session = self.client.session
        session[LANGUAGE_SESSION_KEY] = 'tr'
        session.save()
        self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = 'tr'

        response = self.client.get(reverse('home'))

        self.assertEqual(self.client.session.get(LANGUAGE_SESSION_KEY), 'en')
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, 'en')

    def test_language_cookie_not_rewritten_when_unchanged(self):
        self.user.preferred_language = 'en'
        self.user.save(update_fields=['preferred_language'])
        self.client.force_login(self.user)

        first_response = self.client.get(reverse('home'))
        self.assertEqual(first_response.cookies[settings.LANGUAGE_COOKIE_NAME].value, 'en')

        self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = 'en'
        second_response = self.client.get(reverse('home'))
        self.assertNotIn(settings.LANGUAGE_COOKIE_NAME, second_response.cookies)
