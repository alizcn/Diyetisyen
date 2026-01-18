'use client'

import { useAuth } from '@/lib/hooks/useAuth'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function DietitianPatients() {
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
                <Link href="/dashboard/dietitian/patients" className="text-primary font-medium">Hastalarım</Link>
                <Link href="/dashboard/dietitian/appointments" className="text-secondary-600 hover:text-primary">Randevular</Link>
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
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-secondary-900 mb-2">Hastalarım</h1>
            <p className="text-secondary-600">Tüm hastalarınızı görüntüleyin ve yönetin</p>
          </div>
          <a href="http://localhost:8000/admin" target="_blank" rel="noopener noreferrer" className="btn-primary">
            Admin Panel
          </a>
        </div>

        <div className="card">
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <p className="text-secondary-600 text-sm mb-2">Henüz hastanız yok</p>
            <p className="text-secondary-500 text-xs mb-4">Admin panelden hasta ekleyebilir veya hastalar size atanabilir</p>
            <a href="http://localhost:8000/admin/accounts/patientprofile/" target="_blank" rel="noopener noreferrer" className="btn-primary inline-block">
              Admin Panele Git
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
