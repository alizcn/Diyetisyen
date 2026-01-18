from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from datetime import datetime, date, time
import json

from .models import Appointment
from accounts.models import User
from accounts.decorators import login_required_api


@csrf_exempt
@require_http_methods(["GET"])
@login_required_api
def list_appointments(request):
    """Liste randevuları - hasta veya diyetisyen için"""
    user = request.user

    # Query parameters
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    # Filter appointments based on user type
    if user.user_type == 'patient':
        appointments = Appointment.objects.filter(patient=user)
    elif user.user_type == 'dietitian':
        appointments = Appointment.objects.filter(dietitian=user)
    else:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Apply filters
    if status:
        appointments = appointments.filter(status=status)
    if date_from:
        appointments = appointments.filter(date__gte=date_from)
    if date_to:
        appointments = appointments.filter(date__lte=date_to)

    # Order by date and time
    appointments = appointments.order_by('-date', '-time')

    # Serialize
    data = []
    for apt in appointments:
        data.append({
            'id': apt.id,
            'dietitian': {
                'id': apt.dietitian.id,
                'first_name': apt.dietitian.first_name,
                'last_name': apt.dietitian.last_name,
                'email': apt.dietitian.email,
            },
            'patient': {
                'id': apt.patient.id,
                'first_name': apt.patient.first_name,
                'last_name': apt.patient.last_name,
                'email': apt.patient.email,
            },
            'date': apt.date.isoformat(),
            'time': apt.time.strftime('%H:%M'),
            'duration': apt.duration,
            'status': apt.status,
            'notes': apt.notes,
            'created_at': apt.created_at.isoformat(),
        })

    return JsonResponse({'appointments': data})


@csrf_exempt
@require_http_methods(["POST"])
@login_required_api
def create_appointment(request):
    """Yeni randevu oluştur"""
    user = request.user

    if user.user_type != 'patient':
        return JsonResponse({'error': 'Only patients can create appointments'}, status=403)

    try:
        data = json.loads(request.body)

        # Get dietitian
        dietitian_id = data.get('dietitian_id')
        if not dietitian_id:
            return JsonResponse({'error': 'Dietitian ID is required'}, status=400)

        try:
            dietitian = User.objects.get(id=dietitian_id, user_type='dietitian')
        except User.DoesNotExist:
            return JsonResponse({'error': 'Dietitian not found'}, status=404)

        # Parse date and time
        appointment_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        appointment_time = datetime.strptime(data['time'], '%H:%M').time()

        # Validate date is not in the past
        if appointment_date < date.today():
            return JsonResponse({'error': 'Cannot create appointment in the past'}, status=400)

        # Check for conflicts
        conflicts = Appointment.objects.filter(
            dietitian=dietitian,
            date=appointment_date,
            time=appointment_time,
            status__in=['scheduled', 'confirmed']
        )
        if conflicts.exists():
            return JsonResponse({'error': 'This time slot is already booked'}, status=400)

        # Create appointment
        appointment = Appointment.objects.create(
            dietitian=dietitian,
            patient=user,
            date=appointment_date,
            time=appointment_time,
            duration=data.get('duration', 30),
            status='scheduled',
            notes=data.get('notes', '')
        )

        return JsonResponse({
            'message': 'Appointment created successfully',
            'appointment': {
                'id': appointment.id,
                'dietitian': {
                    'id': dietitian.id,
                    'first_name': dietitian.first_name,
                    'last_name': dietitian.last_name,
                },
                'date': appointment.date.isoformat(),
                'time': appointment.time.strftime('%H:%M'),
                'duration': appointment.duration,
                'status': appointment.status,
                'notes': appointment.notes,
            }
        }, status=201)

    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': f'Invalid data: {str(e)}'}, status=400)


@csrf_exempt
@require_http_methods(["PUT"])
@login_required_api
def update_appointment(request, appointment_id):
    """Randevu güncelle (sadece diyetisyen)"""
    user = request.user

    if user.user_type != 'dietitian':
        return JsonResponse({'error': 'Only dietitians can update appointments'}, status=403)

    try:
        appointment = Appointment.objects.get(id=appointment_id, dietitian=user)
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)

    try:
        data = json.loads(request.body)

        # Update fields
        if 'status' in data:
            appointment.status = data['status']
        if 'notes' in data:
            appointment.notes = data['notes']
        if 'date' in data:
            appointment.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'time' in data:
            appointment.time = datetime.strptime(data['time'], '%H:%M').time()
        if 'duration' in data:
            appointment.duration = data['duration']

        appointment.save()

        return JsonResponse({
            'message': 'Appointment updated successfully',
            'appointment': {
                'id': appointment.id,
                'date': appointment.date.isoformat(),
                'time': appointment.time.strftime('%H:%M'),
                'duration': appointment.duration,
                'status': appointment.status,
                'notes': appointment.notes,
            }
        })

    except ValueError as e:
        return JsonResponse({'error': f'Invalid data: {str(e)}'}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
@login_required_api
def cancel_appointment(request, appointment_id):
    """Randevu iptal et"""
    user = request.user

    try:
        # Hasta veya diyetisyen iptal edebilir
        if user.user_type == 'patient':
            appointment = Appointment.objects.get(id=appointment_id, patient=user)
        elif user.user_type == 'dietitian':
            appointment = Appointment.objects.get(id=appointment_id, dietitian=user)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)

    # Mark as cancelled instead of deleting
    appointment.status = 'cancelled'
    appointment.save()

    return JsonResponse({'message': 'Appointment cancelled successfully'})


@csrf_exempt
@require_http_methods(["GET"])
@login_required_api
def get_appointment(request, appointment_id):
    """Tek randevu detayı"""
    user = request.user

    try:
        if user.user_type == 'patient':
            appointment = Appointment.objects.get(id=appointment_id, patient=user)
        elif user.user_type == 'dietitian':
            appointment = Appointment.objects.get(id=appointment_id, dietitian=user)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)

    return JsonResponse({
        'appointment': {
            'id': appointment.id,
            'dietitian': {
                'id': appointment.dietitian.id,
                'first_name': appointment.dietitian.first_name,
                'last_name': appointment.dietitian.last_name,
                'email': appointment.dietitian.email,
            },
            'patient': {
                'id': appointment.patient.id,
                'first_name': appointment.patient.first_name,
                'last_name': appointment.patient.last_name,
                'email': appointment.patient.email,
            },
            'date': appointment.date.isoformat(),
            'time': appointment.time.strftime('%H:%M'),
            'duration': appointment.duration,
            'status': appointment.status,
            'notes': appointment.notes,
            'created_at': appointment.created_at.isoformat(),
        }
    })
