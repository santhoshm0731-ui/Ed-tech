#accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignupForm
from .models import StudentProfile, TeacherProfile, School

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password1'])
            # optional: save first_name from username or let them edit later
            StudentProfile.objects.create(user=user, year=data['year'], school=data['school'])
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('login')
        # If form invalid, render with errors
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # student or teacher
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # role-based redirect
            if user.is_superuser:
                return redirect('/admin/')
            if role == 'teacher' and hasattr(user, 'teacher_profile') and user.teacher_profile.is_school_admin:
                return redirect('teacher_dashboard')
            if role == 'student' and hasattr(user, 'student_profile'):
                return redirect('student_dashboard')
            # fallback
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
