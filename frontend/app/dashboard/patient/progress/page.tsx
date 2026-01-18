'use client'

import { useAuth } from '@/lib/hooks/useAuth'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function PatientProgress() {
  const { user, loading, logout } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  if (loading || !user) return null

  return (
    <div className="min-h-screen bg-secondary-50">
      <nav className="bg-white border-b border-secondary-200">
        <div className="container-custom">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-8">
              <Link href="/" className="text-2xl font-bold text-primary">Diyetisyen</Link>
              <div className="flex gap-6">
                <Link href="/dashboard/patient" className="text-secondary-600 hover:text-primary">Dashboard</Link>
                <Link href="/dashboard/patient/appointments" className="text-secondary-600 hover:text-primary">Randevularım</Link>
                <Link href="/dashboard/patient/diet-plan" className="text-secondary-600 hover:text-primary">Diyet Planım</Link>
                <Link href="/dashboard/patient/progress" className="text-primary font-medium">İlerleme</Link>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-secondary-600">Hoş geldin, <span className="font-semibold text-secondary-900">{user.first_name}</span></span>
              <button onClick={logout} className="text-sm text-secondary-600 hover:text-primary transition-colors">Çıkış</button>
            </div>
          </div>
        </div>
      </nav>

      <div className="container-custom py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-secondary-900 mb-2">İlerleme Takibi</h1>
            <p className="text-secondary-600">Kilo ve vücut ölçümlerinizi takip edin</p>
          </div>
          <Link href="/dashboard/patient/progress/add" className="btn-primary">
            Ölçüm Ekle
          </Link>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <h3 className="text-sm font-medium text-secondary-600 mb-2">Başlangıç Kilosu</h3>
            <p className="text-2xl font-bold text-secondary-900">80 kg</p>
          </div>
          <div className="card">
            <h3 className="text-sm font-medium text-secondary-600 mb-2">Mevcut Kilo</h3>
            <p className="text-2xl font-bold text-primary">80 kg</p>
          </div>
          <div className="card">
            <h3 className="text-sm font-medium text-secondary-600 mb-2">Hedef Kilo</h3>
            <p className="text-2xl font-bold text-accent">75 kg</p>
          </div>
        </div>

        <div className="card mb-8">
          <h3 className="text-lg font-semibold text-secondary-900 mb-4">Kilo Grafiği</h3>
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <p className="text-secondary-600 text-sm mb-2">Henüz ölçüm kaydınız yok</p>
            <p className="text-secondary-500 text-xs mb-4">Ölçümlerinizi kaydettikçe ilerlemenizi grafikle görebileceksiniz</p>
            <Link href="/dashboard/patient/progress/add" className="btn-primary inline-block">
              İlk Ölçümü Ekle
            </Link>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-secondary-900 mb-4">Ölçüm Geçmişi</h3>
          <div className="text-center py-8">
            <p className="text-secondary-500 text-sm">Ölçüm kaydı bulunamadı</p>
          </div>
        </div>
      </div>
    </div>
  )
}
