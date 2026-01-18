'use client'

import { useAuth } from '@/lib/hooks/useAuth'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

export default function AddMeasurement() {
  const { user, loading, logout } = useAuth()
  const router = useRouter()
  const [formData, setFormData] = useState({
    weight: '',
    body_fat: '',
    muscle_mass: '',
    waist: '',
    hip: '',
    notes: ''
  })

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    alert('Ölçüm kaydı özelliği yakında aktif olacak!')
    router.push('/dashboard/patient/progress')
  }

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
        <div className="max-w-2xl mx-auto">
          <div className="mb-8">
            <Link href="/dashboard/patient/progress" className="text-sm text-secondary-600 hover:text-primary mb-4 inline-block">
              ← Geri dön
            </Link>
            <h1 className="text-3xl font-bold text-secondary-900 mb-2">Ölçüm Ekle</h1>
            <p className="text-secondary-600">Güncel kilo ve vücut ölçülerinizi kaydedin</p>
          </div>

          <form onSubmit={handleSubmit} className="card">
            <div className="space-y-6">
              <div>
                <label htmlFor="weight" className="block text-sm font-medium text-secondary-700 mb-2">
                  Kilo (kg) *
                </label>
                <input
                  id="weight"
                  type="number"
                  step="0.1"
                  required
                  value={formData.weight}
                  onChange={(e) => setFormData({...formData, weight: e.target.value})}
                  className="input-field"
                  placeholder="80.5"
                />
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="body_fat" className="block text-sm font-medium text-secondary-700 mb-2">
                    Yağ Oranı (%)
                  </label>
                  <input
                    id="body_fat"
                    type="number"
                    step="0.1"
                    value={formData.body_fat}
                    onChange={(e) => setFormData({...formData, body_fat: e.target.value})}
                    className="input-field"
                    placeholder="25.0"
                  />
                </div>

                <div>
                  <label htmlFor="muscle_mass" className="block text-sm font-medium text-secondary-700 mb-2">
                    Kas Kütlesi (kg)
                  </label>
                  <input
                    id="muscle_mass"
                    type="number"
                    step="0.1"
                    value={formData.muscle_mass}
                    onChange={(e) => setFormData({...formData, muscle_mass: e.target.value})}
                    className="input-field"
                    placeholder="35.0"
                  />
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="waist" className="block text-sm font-medium text-secondary-700 mb-2">
                    Bel Çevresi (cm)
                  </label>
                  <input
                    id="waist"
                    type="number"
                    step="0.1"
                    value={formData.waist}
                    onChange={(e) => setFormData({...formData, waist: e.target.value})}
                    className="input-field"
                    placeholder="85.0"
                  />
                </div>

                <div>
                  <label htmlFor="hip" className="block text-sm font-medium text-secondary-700 mb-2">
                    Kalça Çevresi (cm)
                  </label>
                  <input
                    id="hip"
                    type="number"
                    step="0.1"
                    value={formData.hip}
                    onChange={(e) => setFormData({...formData, hip: e.target.value})}
                    className="input-field"
                    placeholder="95.0"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="notes" className="block text-sm font-medium text-secondary-700 mb-2">
                  Notlar
                </label>
                <textarea
                  id="notes"
                  rows={3}
                  value={formData.notes}
                  onChange={(e) => setFormData({...formData, notes: e.target.value})}
                  className="input-field"
                  placeholder="Ölçümle ilgili notlarınız..."
                />
              </div>

              <div className="flex gap-4">
                <button type="submit" className="btn-primary flex-1">
                  Ölçümü Kaydet
                </button>
                <Link href="/dashboard/patient/progress" className="btn-secondary flex-1 text-center">
                  İptal
                </Link>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
