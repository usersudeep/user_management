from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth import login
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile = user.profile
            profile.address_line1 = form.cleaned_data.get('address_line1')
            profile.city = form.cleaned_data.get('city')
            profile.state = form.cleaned_data.get('state')
            profile.pincode = form.cleaned_data.get('pincode')
            profile.is_doctor = form.cleaned_data.get('is_doctor')
            profile.profile_picture = request.FILES.get('profile_picture')
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    profile = request.user.profile
    context = {
        'profile': profile
    }
    if profile.is_doctor:
        return render(request, 'accounts/doctor_dashboard.html', context)
    else:
        return render(request, 'accounts/patient_dashboard.html', context)
