'use client'

import { useAuth } from '@/lib/hooks/useAuth'
import { getBackendUrl } from '@/lib/utils'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function DietitianAppointments() {
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
                <Link href="/dashboard/dietitian" className="text-secondary-600 hover:text-primary">Dashboard</Link>
                <Link href="/dashboard/dietitian/patients" className="text-secondary-600 hover:text-primary">Hastalarım</Link>
                <Link href="/dashboard/dietitian/appointments" className="text-primary font-medium">Randevular</Link>
                <Link href="/dashboard/dietitian/diets" className="text-secondary-600 hover:text-primary">Diyet Planları</Link>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-secondary-600">Hoş geldin, <span className="font-semibold text-secondary-900">Dyt. {user.first_name}</span></span>
              <button onClick={logout} className="text-sm text-secondary-600 hover:text-primary transition-colors">Çıkış</button>
            </div>
          </div>
        </div>
      </nav>

      <div className="container-custom py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-secondary-900 mb-2">Randevular</h1>
          <p className="text-secondary-600">Hasta randevularınızı görüntüleyin ve yönetin</p>
        </div>

        <div className="grid gap-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Bugünkü Randevular</h3>
            <div className="text-center py-8">
              <p className="text-secondary-500 text-sm">Bugün randevunuz yok</p>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Yaklaşan Randevular</h3>
            <div className="text-center py-8">
              <p className="text-secondary-500 text-sm">Yaklaşan randevu bulunmuyor</p>
            </div>
          </div>

          <div className="card">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-secondary-900">Tüm Randevular</h3>
              <a href={getBackendUrl('/admin/appointments/appointment/')} target="_blank" rel="noopener noreferrer" className="text-sm text-primary hover:text-primary-600">
                Admin Panelde Yönet →
              </a>
            </div>
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <p className="text-secondary-600 text-sm mb-2">Henüz randevu yok</p>
              <p className="text-secondary-500 text-xs">Hastalar randevu aldığında burada görünecek</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
