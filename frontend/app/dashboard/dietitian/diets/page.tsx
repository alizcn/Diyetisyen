'use client'

import { useAuth } from '@/lib/hooks/useAuth'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function DietitianDiets() {
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
                <Link href="/dashboard/dietitian/appointments" className="text-secondary-600 hover:text-primary">Randevular</Link>
                <Link href="/dashboard/dietitian/diets" className="text-primary font-medium">Diyet Planları</Link>
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
            <h1 className="text-3xl font-bold text-secondary-900 mb-2">Diyet Planları</h1>
            <p className="text-secondary-600">Hastalarınız için oluşturduğunuz beslenme programları</p>
          </div>
          <a href="http://localhost:8000/admin/diets/dietplan/add/" target="_blank" rel="noopener noreferrer" className="btn-primary">
            Yeni Plan Oluştur
          </a>
        </div>

        <div className="grid gap-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Aktif Diyet Planları</h3>
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <p className="text-secondary-600 text-sm mb-2">Henüz diyet planınız yok</p>
              <p className="text-secondary-500 text-xs mb-4">Admin panelden hastalarınız için özelleştirilmiş diyet planları oluşturabilirsiniz</p>
              <a href="http://localhost:8000/admin/diets/dietplan/add/" target="_blank" rel="noopener noreferrer" className="btn-primary inline-block">
                İlk Planı Oluştur
              </a>
            </div>
          </div>

          <div className="card">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-secondary-900">Besin Veritabanı</h3>
              <a href="http://localhost:8000/admin/diets/food/" target="_blank" rel="noopener noreferrer" className="text-sm text-primary hover:text-primary-600">
                Besinleri Yönet →
              </a>
            </div>
            <p className="text-sm text-secondary-600 mb-4">Diyet planlarında kullanılacak besinleri ekleyin ve düzenleyin</p>
            <div className="grid md:grid-cols-3 gap-4">
              <a href="http://localhost:8000/admin/diets/food/add/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 p-3 rounded-lg border border-secondary-200 hover:border-primary transition-colors">
                <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-secondary-900 text-sm">Besin Ekle</p>
                  <p className="text-xs text-secondary-500">Yeni besin kaydı</p>
                </div>
              </a>

              <a href="http://localhost:8000/admin/diets/food/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 p-3 rounded-lg border border-secondary-200 hover:border-primary transition-colors">
                <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-secondary-900 text-sm">Tüm Besinler</p>
                  <p className="text-xs text-secondary-500">Veritabanını görüntüle</p>
                </div>
              </a>

              <a href="http://localhost:8000/admin/diets/meal/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 p-3 rounded-lg border border-secondary-200 hover:border-primary transition-colors">
                <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p className="font-medium text-secondary-900 text-sm">Öğünler</p>
                  <p className="text-xs text-secondary-500">Öğün yönetimi</p>
                </div>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
