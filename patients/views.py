from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date

from .models import Measurement
from accounts.models import PatientProfile


@login_required
def patient_progress(request):
    user = request.user
    if user.user_type != 'patient':
        return redirect('dietitian_dashboard')

    profile, _ = PatientProfile.objects.get_or_create(user=user)
    measurements = Measurement.objects.filter(patient=user).order_by('-date')

    first_weight = None
    if measurements.exists():
        first_measurement = measurements.last()
        first_weight = first_measurement.weight

    return render(request, 'patients/progress.html', {
        'active_page': 'progress',
        'profile': profile,
        'measurements': measurements,
        'first_weight': first_weight,
    })


@login_required
def patient_add_measurement(request):
    user = request.user
    if user.user_type != 'patient':
        return redirect('dietitian_dashboard')

    if request.method == 'POST':
        form_data = {
            'weight': request.POST.get('weight', ''),
            'body_fat': request.POST.get('body_fat', ''),
            'muscle_mass': request.POST.get('muscle_mass', ''),
            'waist': request.POST.get('waist', ''),
            'hip': request.POST.get('hip', ''),
            'chest': request.POST.get('chest', ''),
            'arm': request.POST.get('arm', ''),
            'notes': request.POST.get('notes', ''),
        }

        if not form_data['weight']:
            return render(request, 'patients/add_measurement.html', {
                'active_page': 'progress',
                'error': 'Kilo alanı zorunludur',
                'form_data': form_data,
            })

        today = date.today()
        if Measurement.objects.filter(patient=user, date=today).exists():
            return render(request, 'patients/add_measurement.html', {
                'active_page': 'progress',
                'error': 'Bugün için zaten bir ölçüm kaydınız var',
                'form_data': form_data,
            })

        measurement = Measurement(
            patient=user,
            date=today,
            weight=form_data['weight'],
        )
        if form_data['body_fat']:
            measurement.body_fat_percentage = form_data['body_fat']
        if form_data['muscle_mass']:
            measurement.muscle_mass = form_data['muscle_mass']
        if form_data['waist']:
            measurement.waist_circumference = form_data['waist']
        if form_data['hip']:
            measurement.hip_circumference = form_data['hip']
        if form_data['chest']:
            measurement.chest_circumference = form_data['chest']
        if form_data['arm']:
            measurement.arm_circumference = form_data['arm']
        measurement.notes = form_data['notes']
        measurement.save()

        # Update patient profile current weight
        profile, _ = PatientProfile.objects.get_or_create(user=user)
        profile.current_weight = form_data['weight']
        profile.save()

        messages.success(request, 'Ölçüm başarıyla kaydedildi')
        return redirect('patient_progress')

    return render(request, 'patients/add_measurement.html', {
        'active_page': 'progress',
        'form_data': {},
    })
