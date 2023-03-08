from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Profile


from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from .decorators import *

def map(request):
    profiles = Profile.objects.all()
    points = []
    for profile in profiles:
        if profile.location:
            points.append({
                'lat': profile.location.y,
                'lng': profile.location.x,
            })
    return render(request, 'users/map.html', {'points': points})



@unauthenticated_user
def registration(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        email = request.POST.get('email')

        if User.objects.filter(Q(email__icontains=email)).exists():
            messages.error(request, 'This email is already registered with a different account.')
            return redirect('registration')

        if form.is_valid():
            form.save()
            messages.success(request, f'Account successfully created!')
            return redirect('login')
    context = {'form': form}
    return render(request, 'users/registration.html', context)


@unauthenticated_user
def login_user(request):
    print('\n\n\n\n\n')
    print(request.user)
    print('login_user \n\n\n\n\n')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get('next')

            if next_url == '' or next_url is None:
                next_url = 'base:base-home'
            return redirect(next_url)
        else:
            messages.error(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'users/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('base:base-home')


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password updated successfully!')
            return redirect('password_change')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    context = {'form': form}
    return render(request, 'users/password_change.html', context)


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if user_update_form.is_valid() or profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f'Your account has been updated successfully!')
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=user)
        profile_update_form = ProfileUpdateForm(instance=user.profile)
    context = {'user_update_form': user_update_form, 'profile_update_form': profile_update_form}
    return render(request, 'users/profile.html', context)
