# Diyetisyen Yönetim Sistemi

Django tabanli, diyetisyen ve hasta rollerine sahip bir yonetim uygulamasi.

## Ozellikler

- Coklu rol: `diyetisyen` ve `hasta`
- Session tabanli giris/kayit/cikis
- Hasta randevu olusturma ve iptal
- Diyetisyen randevu yonetimi (tamamlama, iptal)
- Hasta olcum kayitlari ve ilerleme takibi
- Aktif diyet plani goruntuleme
- Docker Compose ile hizli kurulum

## Teknoloji

- Python 3.11+
- Django 4.2+
- PostgreSQL
- Gunicorn
- WhiteNoise (static dosya servisi)
- Bootstrap tabanli Django template UI

## Proje Yapisi

- `config/`: Django ayarlari ve root URL
- `accounts/`: kullanici modeli, auth view'lari, profil modelleri
- `appointments/`: randevu modeli ve akislari
- `patients/`: olcum ve ilerleme akislari
- `diets/`: diyet plani/besin modelleri
- `blog/`: blog modelleri
- `templates/`: tum frontend ekranlari (Django template)

## Hemen Baslat (Docker)

```bash
docker compose up -d --build
```

Uygulama: `http://localhost:8000`

## Lokal Calistirma (opsiyonel)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## Ornek Hesaplar (Mock Data)

Migration ile mock data olusur (`accounts.0003_add_mock_data`).

- Diyetisyen: `ayse@ayse.com` / `ayse`
- Hasta: `elif@patient.com` / `123456`
- Ek test hesaplari migration ile otomatik gelebilir.

## Onemli URL'ler

- Ana sayfa: `/`
- Giris: `/login/`
- Kayit: `/register/`
- Hasta paneli: `/panel/hasta/`
- Diyetisyen paneli: `/panel/diyetisyen/`

## Notlar

- Static dosyalar WhiteNoise ile servis edilir.
- Production ortaminda `DEBUG=False` ve guvenli `SECRET_KEY` kullanin.
- `ALLOWED_HOSTS` ortami degisken ile ayarlanabilir (virgulle ayrilmis).
