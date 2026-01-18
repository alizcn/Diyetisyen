'use client'

import { useAuth } from '@/lib/hooks/useAuth'
import { authAPI } from '@/lib/api/auth'
import { appointmentsAPI } from '@/lib/api/appointments'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

interface Dietitian {
  id: number
  first_name: string
  last_name: string
  email: string
  specialization?: string
}

export default function NewAppointment() {
  const { user, loading, logout } = useAuth()
  const router = useRouter()
  const [dietitians, setDietitians] = useState<Dietitian[]>([])
  const [loadingDietitians, setLoadingDietitians] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    dietitian_id: '',
    date: '',
    time: '09:00',
    notes: ''
  })

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  useEffect(() => {
    loadDietitians()
  }, [])

  const loadDietitians = async () => {
    try {
      const data = await authAPI.listDietitians()
      setDietitians(data.dietitians)
    } catch (err) {
      console.error('Failed to load dietitians:', err)
    } finally {
      setLoadingDietitians(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSubmitting(true)

    try {
      await appointmentsAPI.create({
        dietitian_id: parseInt(formData.dietitian_id),
        date: formData.date,
        time: formData.time,
        duration: 30,
        notes: formData.notes
      })

      // Success - redirect to appointments list
      router.push('/dashboard/patient/appointments')
    } catch (err: any) {
      setError(err.response?.data?.error || 'Randevu oluşturulurken bir hata oluştu')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading || !user) return null

  // Get tomorrow's date as minimum
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  const minDate = tomorrow.toISOString().split('T')[0]

  return (
    <div className="min-h-screen bg-secondary-50">
      <nav className="bg-white border-b border-secondary-200">
        <div className="container-custom">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-8">
              <Link href="/" className="text-2xl font-bold text-primary">Diyetisyen</Link>
              <div className="flex gap-6">
                <Link href="/dashboard/patient" className="text-secondary-600 hover:text-primary">Dashboard</Link>
                <Link href="/dashboard/patient/appointments" className="text-primary font-medium">Randevularım</Link>
                <Link href="/dashboard/patient/diet-plan" className="text-secondary-600 hover:text-primary">Diyet Planım</Link>
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
        <div className="max-w-2xl mx-auto">
          <div className="mb-8">
            <Link href="/dashboard/patient/appointments" className="text-sm text-secondary-600 hover:text-primary mb-4 inline-block">
              ← Geri dön
            </Link>
            <h1 className="text-3xl font-bold text-secondary-900 mb-2">Yeni Randevu Al</h1>
            <p className="text-secondary-600">Diyetisyen seçin ve randevu tarihi belirleyin</p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="card">
            <div className="space-y-6">
              <div>
                <label htmlFor="dietitian_id" className="block text-sm font-medium text-secondary-700 mb-2">
                  Diyetisyen Seçin *
                </label>
                {loadingDietitians ? (
                  <div className="text-sm text-secondary-500">Diyetisyenler yükleniyor...</div>
                ) : (
                  <select
                    id="dietitian_id"
                    required
                    value={formData.dietitian_id}
                    onChange={(e) => setFormData({...formData, dietitian_id: e.target.value})}
                    className="input-field"
                  >
                    <option value="">Diyetisyen seçin...</option>
                    {dietitians.map((dietitian) => (
                      <option key={dietitian.id} value={dietitian.id}>
                        Dyt. {dietitian.first_name} {dietitian.last_name}
                        {dietitian.specialization && ` - ${dietitian.specialization}`}
                      </option>
                    ))}
                  </select>
                )}
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="date" className="block text-sm font-medium text-secondary-700 mb-2">
                    Tarih *
                  </label>
                  <input
                    id="date"
                    type="date"
                    required
                    min={minDate}
                    value={formData.date}
                    onChange={(e) => setFormData({...formData, date: e.target.value})}
                    className="input-field"
                  />
                </div>

                <div>
                  <label htmlFor="time" className="block text-sm font-medium text-secondary-700 mb-2">
                    Saat *
                  </label>
                  <select
                    id="time"
                    required
                    value={formData.time}
                    onChange={(e) => setFormData({...formData, time: e.target.value})}
                    className="input-field"
                  >
                    <option value="09:00">09:00</option>
                    <option value="09:30">09:30</option>
                    <option value="10:00">10:00</option>
                    <option value="10:30">10:30</option>
                    <option value="11:00">11:00</option>
                    <option value="11:30">11:30</option>
                    <option value="12:00">12:00</option>
                    <option value="13:00">13:00</option>
                    <option value="13:30">13:30</option>
                    <option value="14:00">14:00</option>
                    <option value="14:30">14:30</option>
                    <option value="15:00">15:00</option>
                    <option value="15:30">15:30</option>
                    <option value="16:00">16:00</option>
                    <option value="16:30">16:30</option>
                    <option value="17:00">17:00</option>
                  </select>
                </div>
              </div>

              <div>
                <label htmlFor="notes" className="block text-sm font-medium text-secondary-700 mb-2">
                  Notlar (Opsiyonel)
                </label>
                <textarea
                  id="notes"
                  rows={3}
                  value={formData.notes}
                  onChange={(e) => setFormData({...formData, notes: e.target.value})}
                  className="input-field"
                  placeholder="Randevuyla ilgili notlarınız..."
                />
              </div>

              <div className="flex gap-4">
                <button
                  type="submit"
                  disabled={submitting}
                  className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {submitting ? 'Oluşturuluyor...' : 'Randevu Oluştur'}
                </button>
                <Link href="/dashboard/patient/appointments" className="btn-secondary flex-1 text-center">
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
