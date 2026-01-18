'use client'

import { useAuth } from '@/lib/hooks/useAuth'
import { appointmentsAPI, Appointment } from '@/lib/api/appointments'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

export default function PatientAppointments() {
  const { user, loading, logout } = useAuth()
  const router = useRouter()
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [loadingAppointments, setLoadingAppointments] = useState(true)

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  useEffect(() => {
    if (user) {
      loadAppointments()
    }
  }, [user])

  const loadAppointments = async () => {
    try {
      const data = await appointmentsAPI.list()
      setAppointments(data.appointments)
    } catch (err) {
      console.error('Failed to load appointments:', err)
    } finally {
      setLoadingAppointments(false)
    }
  }

  const handleCancel = async (id: number) => {
    if (!confirm('Bu randevuyu iptal etmek istediğinizden emin misiniz?')) {
      return
    }

    try {
      await appointmentsAPI.cancel(id)
      // Reload appointments
      loadAppointments()
    } catch (err) {
      console.error('Failed to cancel appointment:', err)
      alert('Randevu iptal edilirken bir hata oluştu')
    }
  }

  const getStatusBadge = (status: string) => {
    const badges = {
      scheduled: 'bg-blue-100 text-blue-800',
      confirmed: 'bg-green-100 text-green-800',
      completed: 'bg-gray-100 text-gray-800',
      cancelled: 'bg-red-100 text-red-800',
    }
    const labels = {
      scheduled: 'Planlandı',
      confirmed: 'Onaylandı',
      completed: 'Tamamlandı',
      cancelled: 'İptal Edildi',
    }
    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full ${badges[status as keyof typeof badges] || 'bg-gray-100 text-gray-800'}`}>
        {labels[status as keyof typeof labels] || status}
      </span>
    )
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return date.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' })
  }

  if (loading || !user) return null

  const activeAppointments = appointments.filter(a => a.status !== 'cancelled' && a.status !== 'completed')
  const pastAppointments = appointments.filter(a => a.status === 'cancelled' || a.status === 'completed')

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
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-secondary-900 mb-2">Randevularım</h1>
            <p className="text-secondary-600">Geçmiş ve yaklaşan randevularınızı görüntüleyin</p>
          </div>
          <Link href="/dashboard/patient/appointments/new" className="btn-primary">
            Yeni Randevu Al
          </Link>
        </div>

        {loadingAppointments ? (
          <div className="card">
            <div className="text-center py-12">
              <p className="text-secondary-500">Yükleniyor...</p>
            </div>
          </div>
        ) : appointments.length === 0 ? (
          <div className="card">
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <p className="text-secondary-600 text-sm mb-2">Henüz randevunuz yok</p>
              <p className="text-secondary-500 text-xs mb-4">Bir diyetisyen seçerek ilk randevunuzu oluşturun</p>
              <Link href="/dashboard/patient/appointments/new" className="btn-primary inline-block">
                Randevu Al
              </Link>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {activeAppointments.length > 0 && (
              <div className="card">
                <h2 className="text-xl font-semibold text-secondary-900 mb-4">Yaklaşan Randevular</h2>
                <div className="space-y-4">
                  {activeAppointments.map((appointment) => (
                    <div key={appointment.id} className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg border border-secondary-200">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="font-semibold text-secondary-900">
                            Dyt. {appointment.dietitian.first_name} {appointment.dietitian.last_name}
                          </h3>
                          {getStatusBadge(appointment.status)}
                        </div>
                        <div className="flex items-center gap-4 text-sm text-secondary-600">
                          <span className="flex items-center gap-1">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            {formatDate(appointment.date)}
                          </span>
                          <span className="flex items-center gap-1">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            {appointment.time} ({appointment.duration} dk)
                          </span>
                        </div>
                        {appointment.notes && (
                          <p className="text-sm text-secondary-500 mt-2">{appointment.notes}</p>
                        )}
                      </div>
                      {appointment.status === 'scheduled' && (
                        <button
                          onClick={() => handleCancel(appointment.id)}
                          className="ml-4 px-4 py-2 text-sm text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors"
                        >
                          İptal Et
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {pastAppointments.length > 0 && (
              <div className="card">
                <h2 className="text-xl font-semibold text-secondary-900 mb-4">Geçmiş Randevular</h2>
                <div className="space-y-4">
                  {pastAppointments.map((appointment) => (
                    <div key={appointment.id} className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg border border-secondary-200 opacity-75">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="font-semibold text-secondary-900">
                            Dyt. {appointment.dietitian.first_name} {appointment.dietitian.last_name}
                          </h3>
                          {getStatusBadge(appointment.status)}
                        </div>
                        <div className="flex items-center gap-4 text-sm text-secondary-600">
                          <span>{formatDate(appointment.date)}</span>
                          <span>{appointment.time}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
