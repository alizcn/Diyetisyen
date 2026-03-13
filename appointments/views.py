from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from datetime import datetime, date, timedelta

from .models import Appointment
from accounts.models import User


TIME_SLOTS = [
    '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
    '12:00', '13:00', '13:30', '14:00', '14:30',
    '15:00', '15:30', '16:00', '16:30', '17:00',
]


@login_required
def patient_appointments(request):
    user = request.user
    if user.user_type != 'patient':
        return redirect('dietitian_appointments')

    appointments = Appointment.objects.filter(patient=user).order_by('-date', '-time')
    active_appointments = [a for a in appointments if a.status not in ('cancelled', 'completed')]
    past_appointments = [a for a in appointments if a.status in ('cancelled', 'completed')]

    return render(request, 'appointments/patient_list.html', {
        'active_page': 'appointments',
        'appointments': appointments,
        'active_appointments': active_appointments,
        'past_appointments': past_appointments,
    })


@login_required
def patient_appointment_new(request):
    user = request.user
    if user.user_type != 'patient':
        return redirect('dietitian_dashboard')

    tomorrow = date.today() + timedelta(days=1)
    min_date = tomorrow.strftime('%Y-%m-%d')
    dietitians = User.objects.filter(user_type='dietitian', is_active=True).select_related('dietitian_profile')

    if request.method == 'POST':
        form_data = {
            'dietitian_id': request.POST.get('dietitian_id', ''),
            'date': request.POST.get('date', ''),
            'time': request.POST.get('time', '09:00'),
            'notes': request.POST.get('notes', ''),
        }

        if not form_data['dietitian_id'] or not form_data['date']:
            return render(request, 'appointments/patient_new.html', {
                'active_page': 'appointments',
                'error': _('Diyetisyen ve tarih seçimi zorunludur'),
                'dietitians': dietitians,
                'form_data': form_data,
                'min_date': min_date,
                'time_slots': TIME_SLOTS,
            })

        try:
            dietitian = User.objects.get(id=form_data['dietitian_id'], user_type='dietitian')
        except User.DoesNotExist:
            return render(request, 'appointments/patient_new.html', {
                'active_page': 'appointments',
                'error': _('Diyetisyen bulunamadı'),
                'dietitians': dietitians,
                'form_data': form_data,
                'min_date': min_date,
                'time_slots': TIME_SLOTS,
            })

        try:
            appointment_date = datetime.strptime(form_data['date'], '%Y-%m-%d').date()
            appointment_time = datetime.strptime(form_data['time'], '%H:%M').time()
        except ValueError:
            return render(request, 'appointments/patient_new.html', {
                'active_page': 'appointments',
                'error': _('Tarih veya saat formatı geçersiz'),
                'dietitians': dietitians,
                'form_data': form_data,
                'min_date': min_date,
                'time_slots': TIME_SLOTS,
            })

        if appointment_date < date.today():
            return render(request, 'appointments/patient_new.html', {
                'active_page': 'appointments',
                'error': _('Geçmiş bir tarihe randevu oluşturulamaz'),
                'dietitians': dietitians,
                'form_data': form_data,
                'min_date': min_date,
                'time_slots': TIME_SLOTS,
            })

        conflicts = Appointment.objects.filter(
            dietitian=dietitian, date=appointment_date, time=appointment_time,
            status__in=['scheduled', 'confirmed']
        )
        if conflicts.exists():
            return render(request, 'appointments/patient_new.html', {
                'active_page': 'appointments',
                'error': _('Bu saat dilimi zaten dolu'),
                'dietitians': dietitians,
                'form_data': form_data,
                'min_date': min_date,
                'time_slots': TIME_SLOTS,
            })

        Appointment.objects.create(
            dietitian=dietitian,
            patient=user,
            date=appointment_date,
            time=appointment_time,
            duration=30,
            status='scheduled',
            notes=form_data['notes']
        )

        messages.success(request, _('Randevu başarıyla oluşturuldu'))
        return redirect('patient_appointments')

    return render(request, 'appointments/patient_new.html', {
        'active_page': 'appointments',
        'dietitians': dietitians,
        'form_data': {'time': '09:00'},
        'min_date': min_date,
        'time_slots': TIME_SLOTS,
    })


@login_required
def patient_appointment_cancel(request, appointment_id):
    if request.method != 'POST':
        return redirect('patient_appointments')

    user = request.user
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=user)
    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request, _('Randevu iptal edildi'))
    return redirect('patient_appointments')


# ==================== DIETITIAN APPOINTMENT VIEWS ====================

@login_required
def dietitian_appointments(request):
    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_appointments')

    today = date.today()
    today_appointments = Appointment.objects.filter(
        dietitian=user, date=today
    ).exclude(status='cancelled').order_by('time')

    upcoming_appointments = Appointment.objects.filter(
        dietitian=user, date__gt=today, status='scheduled'
    ).order_by('date', 'time')

    all_appointments = Appointment.objects.filter(dietitian=user).order_by('-date', '-time')

    return render(request, 'dietitian/appointments.html', {
        'active_page': 'appointments',
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'all_appointments': all_appointments,
    })


@login_required
def dietitian_appointment_update(request, appointment_id):
    if request.method != 'POST':
        return redirect('dietitian_appointments')

    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    appointment = get_object_or_404(Appointment, id=appointment_id, dietitian=user)
    status = request.POST.get('status')
    if status in ('completed', 'confirmed', 'scheduled'):
        appointment.status = status
        try:
            appointment.save()
            messages.success(request, _('Randevu güncellendi'))
        except ValidationError as exc:
            messages.error(request, _('Randevu güncellenemedi: %(error)s') % {'error': exc})

    return redirect('dietitian_appointments')


@login_required
def dietitian_appointment_cancel(request, appointment_id):
    if request.method != 'POST':
        return redirect('dietitian_appointments')

    user = request.user
    if user.user_type != 'dietitian':
        return redirect('patient_dashboard')

    appointment = get_object_or_404(Appointment, id=appointment_id, dietitian=user)
    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request, _('Randevu iptal edildi'))
    return redirect('dietitian_appointments')
