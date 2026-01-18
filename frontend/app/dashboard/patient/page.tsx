'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/hooks/useAuth'
import Link from 'next/link'

export default function PatientDashboard() {
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

  if (!user || user.user_type !== 'patient') {
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
                <Link href="/dashboard/patient" className="text-primary font-medium">
                  Dashboard
                </Link>
                <Link href="/dashboard/patient/appointments" className="text-secondary-600 hover:text-primary">
                  Randevularım
                </Link>
                <Link href="/dashboard/patient/diet-plan" className="text-secondary-600 hover:text-primary">
                  Diyet Planım
                </Link>
                <Link href="/dashboard/patient/progress" className="text-secondary-600 hover:text-primary">
                  İlerleme
                </Link>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-secondary-600">
                Hoş geldin, <span className="font-semibold text-secondary-900">{user.first_name}</span>
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
            Hasta Paneli
          </h1>
          <p className="text-secondary-600">
            Sağlıklı yaşam yolculuğunuzu takip edin
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-secondary-600">Mevcut Kilo</h3>
              <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                </svg>
              </div>
            </div>
            <p className="text-2xl font-bold text-secondary-900">80 kg</p>
            <p className="text-xs text-secondary-500 mt-1">Hedef: 75 kg</p>
          </div>

          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-secondary-600">BMI</h3>
              <div className="w-10 h-10 bg-accent-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
            </div>
            <p className="text-2xl font-bold text-secondary-900">26.1</p>
            <p className="text-xs text-accent-600 mt-1">Hafif Kilolu</p>
          </div>

          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-secondary-600">Yaklaşan Randevu</h3>
              <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <p className="text-2xl font-bold text-secondary-900">-</p>
            <p className="text-xs text-secondary-500 mt-1">Randevu alın</p>
          </div>

          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-secondary-600">Aktif Diyet</h3>
              <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
            </div>
            <p className="text-2xl font-bold text-secondary-900">-</p>
            <p className="text-xs text-secondary-500 mt-1">Plan bekleniyor</p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Hızlı İşlemler</h3>
            <div className="space-y-3">
              <Link href="/dashboard/patient/appointments/new" className="flex items-center gap-3 p-3 rounded-lg hover:bg-secondary-50 transition-colors">
                <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-secondary-900">Randevu Al</p>
                  <p className="text-sm text-secondary-500">Diyetisyeninizle görüşün</p>
                </div>
              </Link>

              <Link href="/dashboard/patient/progress/add" className="flex items-center gap-3 p-3 rounded-lg hover:bg-secondary-50 transition-colors">
                <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-secondary-900">Ölçüm Kaydet</p>
                  <p className="text-sm text-secondary-500">Kilo ve vücut ölçülerinizi girin</p>
                </div>
              </Link>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Profil Bilgileri</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center pb-3 border-b border-secondary-100">
                <span className="text-sm text-secondary-600">Ad Soyad</span>
                <span className="text-sm font-medium text-secondary-900">{user.first_name} {user.last_name}</span>
              </div>
              <div className="flex justify-between items-center pb-3 border-b border-secondary-100">
                <span className="text-sm text-secondary-600">Email</span>
                <span className="text-sm font-medium text-secondary-900">{user.email}</span>
              </div>
              <div className="flex justify-between items-center pb-3 border-b border-secondary-100">
                <span className="text-sm text-secondary-600">Boy</span>
                <span className="text-sm font-medium text-secondary-900">175 cm</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-secondary-600">Diyetisyen</span>
                <span className="text-sm font-medium text-secondary-900">Atanmadı</span>
              </div>
            </div>
          </div>
        </div>

        {/* Welcome Message */}
        <div className="mt-8 card bg-gradient-to-r from-primary-50 to-primary-100 border-primary-200">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 className="font-semibold text-secondary-900 mb-2">Hoş Geldiniz!</h3>
              <p className="text-sm text-secondary-600">
                Sağlıklı yaşam yolculuğunuza başlamak için bir diyetisyen seçin ve randevu alın.
                Düzenli ölçümlerinizi kaydetmeyi unutmayın!
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
