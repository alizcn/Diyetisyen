from django.contrib import admin
from django.urls import include, path
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
    path('language/set/', accounts_views.set_language_preference, name='set_language_preference'),

    # Patient pages
    path('panel/hasta/', accounts_views.patient_dashboard, name='patient_dashboard'),
    path('panel/hasta/diyet-plani/', accounts_views.patient_diet_plan, name='patient_diet_plan'),
    path('panel/hasta/randevular/', include('appointments.urls_patient')),
    path('panel/hasta/ilerleme/', include('patients.urls')),

    # Dietitian pages
    path('panel/diyetisyen/', accounts_views.dietitian_dashboard, name='dietitian_dashboard'),
    path('panel/diyetisyen/profil/', accounts_views.dietitian_profile_edit, name='dietitian_profile_edit'),
    path('panel/diyetisyen/hastalar/', accounts_views.dietitian_patients, name='dietitian_patients'),
    path('panel/diyetisyen/hastalar/<int:patient_id>/duzenle/', accounts_views.dietitian_patient_edit, name='dietitian_patient_edit'),
    path('panel/diyetisyen/hastalar/<int:patient_id>/sil/', accounts_views.dietitian_patient_delete, name='dietitian_patient_delete'),
    path('panel/diyetisyen/diyet-planlari/', accounts_views.dietitian_diets, name='dietitian_diets'),
    path('panel/diyetisyen/diyet-planlari/yeni/', accounts_views.dietitian_diet_create, name='dietitian_diet_create'),
    path('panel/diyetisyen/diyet-planlari/<int:plan_id>/duzenle/', accounts_views.dietitian_diet_edit, name='dietitian_diet_edit'),
    path('panel/diyetisyen/diyet-planlari/<int:plan_id>/sil/', accounts_views.dietitian_diet_delete, name='dietitian_diet_delete'),
    path('panel/diyetisyen/besinler/ekle/', accounts_views.dietitian_food_create, name='dietitian_food_create'),
    path('panel/diyetisyen/besinler/<int:food_id>/duzenle/', accounts_views.dietitian_food_edit, name='dietitian_food_edit'),
    path('panel/diyetisyen/besinler/<int:food_id>/sil/', accounts_views.dietitian_food_delete, name='dietitian_food_delete'),
    path('panel/diyetisyen/randevular/', include('appointments.urls_dietitian')),

    # API endpoints (kept for backward compat)
    path('api/auth/dietitians/', accounts_views.list_dietitians, name='list_dietitians'),
]

# Media dosyaları için development ayarı
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
