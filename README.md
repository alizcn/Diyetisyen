# Profesyonel Diyetisyen Yönetim Sistemi

Modern ve kullanıcı dostu bir diyetisyen-hasta yönetim platformu.

## Özellikler

- ✅ **Multi-User Sistem**: Diyetisyen ve hasta rolleri
- ✅ **Randevu Yönetimi**: Online randevu alma ve yönetme
- ✅ **Hasta Takibi**: Kilo, vücut ölçümleri, ilerleme grafikleri
- ✅ **Diyet Planları**: Özelleştirilmiş beslenme programları
- ✅ **Blog Sistemi**: Beslenme ve sağlık içerikleri
- ✅ **Modern Tasarım**: Tailwind CSS ile minimal ve profesyonel arayüz

## Teknoloji Stack

### Backend
- Django 4.2+
- SQLite3 Database
- JWT Authentication
- Python 3.13

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Axios
- React Hooks

## Kurulum

### Backend Kurulumu

```bash
cd backend

# Virtual environment oluştur (önerilir)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Paketleri kur
pip install -r requirements.txt

# Veritabanını oluştur
python manage.py migrate

# Superuser oluştur
python manage.py createsuperuser

# Development server'ı başlat
python manage.py runserver
```

Backend http://localhost:8000 adresinde çalışacak.
Admin panel: http://localhost:8000/admin

### Frontend Kurulumu

```bash
cd frontend

# Paketleri kur
npm install

# Development server'ı başlat
npm run dev
```

Frontend http://localhost:3000 adresinde çalışacak.

## Kullanım

1. Backend'i çalıştırın: `cd backend && python manage.py runserver`
2. Frontend'i çalıştırın: `cd frontend && npm run dev`
3. Tarayıcıda http://localhost:3000 adresine gidin
4. Yeni bir hesap oluşturun (Diyetisyen veya Hasta)
5. Dashboard'a erişin ve özellikleri keşfedin

## Proje Yapısı

```
diyetisyen/
├── backend/
│   ├── config/              # Django ayarları
│   ├── accounts/            # Kullanıcı yönetimi
│   ├── appointments/        # Randevu sistemi
│   ├── patients/            # Hasta takibi
│   ├── diets/               # Diyet planları
│   ├── blog/                # Blog sistemi
│   └── db.sqlite3           # Veritabanı
├── frontend/
│   ├── app/                 # Next.js pages
│   ├── components/          # React components
│   ├── lib/                 # Utilities, hooks, API
│   └── public/              # Static files
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Kullanıcı kaydı
- `POST /api/auth/login/` - Giriş
- `GET /api/auth/me/` - Kullanıcı bilgileri
- `PUT /api/auth/profile/` - Profil güncelleme
- `GET /api/auth/dietitians/` - Diyetisyen listesi

### Diğer Endpoints
*(Geliştirme aşamasında)*
- Appointments API
- Patients/Measurements API
- Diet Plans API
- Blog API

## Lisans

Bu proje eğitim amaçlıdır.

## Destek

Sorularınız için GitHub Issues kullanabilirsiniz.
