from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Public pages
    path('', accounts_views.home, name='home'),
    path('login/', accounts_views.login_view, name='login'),
    path('register/', accounts_views.register_view, name='register'),
    path('logout/', accounts_views.logout_view, name='logout'),

    # Patient pages
    path('panel/hasta/', accounts_views.patient_dashboard, name='patient_dashboard'),
    path('panel/hasta/diyet-plani/', accounts_views.patient_diet_plan, name='patient_diet_plan'),
    path('panel/hasta/randevular/', include('appointments.urls_patient')),
    path('panel/hasta/ilerleme/', include('patients.urls')),

    # Dietitian pages
    path('panel/diyetisyen/', accounts_views.dietitian_dashboard, name='dietitian_dashboard'),
    path('panel/diyetisyen/hastalar/', accounts_views.dietitian_patients, name='dietitian_patients'),
    path('panel/diyetisyen/diyet-planlari/', accounts_views.dietitian_diets, name='dietitian_diets'),
    path('panel/diyetisyen/randevular/', include('appointments.urls_dietitian')),

    # API endpoints (kept for backward compat)
    path('api/auth/dietitians/', accounts_views.list_dietitians, name='list_dietitians'),
]

# Media dosyaları için development ayarı
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
