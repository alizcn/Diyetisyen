'use client'

import { useAuth } from '@/lib/hooks/useAuth'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function PatientDietPlan() {
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
                <Link href="/dashboard/patient/diet-plan" className="text-primary font-medium">Diyet Planım</Link>
                <Link href="/dashboard/patient/progress" className="text-secondary-600 hover:text-primary">İlerleme</Link>
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
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-secondary-900 mb-2">Diyet Planım</h1>
          <p className="text-secondary-600">Diyetisyeniniz tarafından oluşturulan beslenme programınız</p>
        </div>

        <div className="card">
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <p className="text-secondary-600 text-sm mb-2">Henüz diyet planınız yok</p>
            <p className="text-secondary-500 text-xs">Diyetisyeniniz size özel bir plan oluşturduğunda burada görünecek</p>
          </div>
        </div>
      </div>
    </div>
  )
}
