from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignupForm, TeacherSignupForm
from .models import StudentProfile, TeacherProfile
from django.contrib.auth import authenticate, login, logout


def student_signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password1'])
            StudentProfile.objects.create(user=user, year=data['year'], school=data['school'])
            messages.success(request, 'Student account created. Please login.')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def teacher_signup_view(request):
    if request.method == 'POST':
        form = TeacherSignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            school = data['school']

            if TeacherProfile.objects.filter(school=school).exists():
                form.add_error('school', f"{school.name} already has a teacher-admin.")
            else:
                user = User.objects.create_user(username=data['username'], email=data['email'],
                                                password=data['password1'])
                TeacherProfile.objects.create(user=user, school=school)
                messages.success(request, 'Teacher account created. Please login.')
                return redirect('login')
    else:
        form = TeacherSignupForm()
    return render(request, 'accounts/teacher_signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  # 'student' or 'teacher'

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If superuser, redirect to Django admin
            if user.is_superuser:
                login(request, user)
                return redirect('/admin/')

            # Check user type matches profile
            if user_type == 'student' and not hasattr(user, 'student_profile'):
                messages.error(request, "This account is not a student account.")
                return redirect('login')
            if user_type == 'teacher' and not hasattr(user, 'teacher_profile'):
                messages.error(request, "This account is not a teacher account.")
                return redirect('login')

            login(request, user)
            if user_type == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'accounts/login.html')



@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')
