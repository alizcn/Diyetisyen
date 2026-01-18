'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/hooks/useAuth'
import { getBackendUrl } from '@/lib/utils'
import Link from 'next/link'

export default function DietitianDashboard() {
  const { user, loading, logout } = useAuth()
  const router = useRouter()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  if (loading || !mounted) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-secondary-600">Yükleniyor...</p>
        </div>
      </div>
    )
  }

  if (!user || user.user_type !== 'dietitian') {
    return null
  }

  return (
    <div className="min-h-screen bg-secondary-50">
      {/* Navbar */}
      <nav className="bg-white border-b border-secondary-200">
        <div className="container-custom">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-8">
              <Link href="/" className="text-2xl font-bold text-primary">
                Diyetisyen
              </Link>
              <div className="flex gap-6">
                <Link href="/dashboard/dietitian" className="text-primary font-medium">
                  Dashboard
                </Link>
                <Link href="/dashboard/dietitian/patients" className="text-secondary-600 hover:text-primary">
                  Hastalarım
                </Link>
                <Link href="/dashboard/dietitian/appointments" className="text-secondary-600 hover:text-primary">
                  Randevular
                </Link>
                <Link href="/dashboard/dietitian/diets" className="text-secondary-600 hover:text-primary">
                  Diyet Planları
                </Link>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-secondary-600">
                Hoş geldin, <span className="font-semibold text-secondary-900">Dyt. {user.first_name}</span>
              </span>
              <button
                onClick={logout}
                className="text-sm text-secondary-600 hover:text-primary transition-colors"
              >
                Çıkış
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container-custom py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-secondary-900 mb-2">
            Diyetisyen Paneli
          </h1>
          <p className="text-secondary-600">
            Hastalarınızı yönetin ve ilerlemeyi takip edin
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-secondary-600">Toplam Hasta</h3>
              <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
            </div>
            <p className="text-2xl font-bold text-secondary-900">0</p>
            <p className="text-xs text-secondary-500 mt-1">Aktif hastalar</p>
          </div>

          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-secondary-600">Bugünkü Randevular</h3>
              <div className="w-10 h-10 bg-accent-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <p className="text-2xl font-bold text-secondary-900">0</p>
            <p className="text-xs text-secondary-500 mt-1">Randevu yok</p>
          </div>

          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-secondary-600">Aktif Diyet Planı</h3>
              <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
            </div>
            <p className="text-2xl font-bold text-secondary-900">0</p>
            <p className="text-xs text-secondary-500 mt-1">Oluşturulan plan</p>
          </div>

          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-secondary-600">Başarı Oranı</h3>
              <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
            </div>
            <p className="text-2xl font-bold text-secondary-900">-</p>
            <p className="text-xs text-secondary-500 mt-1">Veri yok</p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="card">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Hızlı İşlemler</h3>
            <div className="space-y-3">
              <Link href="/dashboard/dietitian/patients/new" className="flex items-center gap-3 p-3 rounded-lg hover:bg-secondary-50 transition-colors">
                <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-secondary-900">Yeni Hasta Ekle</p>
                  <p className="text-sm text-secondary-500">Hasta kaydı oluştur</p>
                </div>
              </Link>

              <Link href="/dashboard/dietitian/diets/new" className="flex items-center gap-3 p-3 rounded-lg hover:bg-secondary-50 transition-colors">
                <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-secondary-900">Diyet Planı Oluştur</p>
                  <p className="text-sm text-secondary-500">Yeni beslenme programı</p>
                </div>
              </Link>

              <Link href="/admin" className="flex items-center gap-3 p-3 rounded-lg hover:bg-secondary-50 transition-colors">
                <div className="w-10 h-10 bg-accent-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-secondary-900">Admin Panel</p>
                  <p className="text-sm text-secondary-500">Gelişmiş yönetim</p>
                </div>
              </Link>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Yaklaşan Randevular</h3>
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <p className="text-secondary-600 text-sm">Henüz randevu yok</p>
              <p className="text-secondary-500 text-xs mt-1">Hastalar randevu aldığında burada görünecek</p>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="card">
          <h3 className="text-lg font-semibold text-secondary-900 mb-4">Son Aktiviteler</h3>
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-secondary-600 text-sm">Henüz aktivite yok</p>
            <p className="text-secondary-500 text-xs mt-1">Hasta etkileşimleri burada görünecek</p>
          </div>
        </div>

        {/* Welcome Message */}
        <div className="mt-8 card bg-gradient-to-r from-primary-50 to-primary-100 border-primary-200">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 className="font-semibold text-secondary-900 mb-2">Admin Paneli</h3>
              <p className="text-sm text-secondary-600 mb-3">
                Daha gelişmiş yönetim özellikleri için Django Admin Panelini kullanabilirsiniz.
                Buradan hasta ekleyebilir, diyet planları oluşturabilir ve tüm verileri yönetebilirsiniz.
              </p>
              <a
                href={getBackendUrl('/admin')}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 text-sm font-medium text-primary hover:text-primary-600 transition-colors"
              >
                Admin Paneline Git
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
