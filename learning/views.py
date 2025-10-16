from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Level
from accounts.models import StudentProfile, TeacherProfile

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def home_view(request):
    return render(request, 'home.html')


def home_redirect(request):
    """
    Landing page / home page view.
    - If user is logged in, redirect to their dashboard.
    - If not logged in, show home.html.
    """
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser:
            return redirect('/admin/')
        if hasattr(user, 'teacher_profile') and user.teacher_profile.is_school_admin:
            return redirect('teacher_dashboard')
        if hasattr(user, 'student_profile'):
            return redirect('student_dashboard')
    return render(request, 'home.html')


@login_required
def student_dashboard(request):
    profile = getattr(request.user, 'student_profile', None)
    levels = Level.objects.all()
    return render(request, 'learning/student_dashboard.html', {'profile': profile, 'levels': levels})


@login_required
def teacher_dashboard(request):
    tp = getattr(request.user, 'teacher_profile', None)
    if not tp or not tp.is_school_admin:
        messages.error(request, 'Not authorized')
        return redirect('login')
    students = tp.school.students.filter(is_active=True).order_by('-points')
    return render(request, 'learning/teacher_dashboard.html', {'students': students})


@login_required
def level1_view(request):
    level = Level.objects.filter(number=1).first()
    return render(request, 'learning/level1.html', {'level': level})


@login_required
def level2_view(request):
    level = Level.objects.filter(number=2).first()
    quiz = level.quizzes.first() if level else None
    return render(request, 'learning/level2.html', {'level': level, 'quiz': quiz})


@login_required
@csrf_exempt
def award_points(request):
    if request.method == 'POST':
        try:
            points = int(request.POST.get('points', 0))
        except:
            points = 0
        profile = getattr(request.user, 'student_profile', None)
        if not profile:
            return JsonResponse({'status': 'error', 'message': 'No student profile'}, status=400)
        profile.points += points
        if profile.points >= 100:
            profile.current_level = 3
        elif profile.points >= 50:
            profile.current_level = 2
        profile.save()
        return JsonResponse({'status': 'ok', 'points': profile.points, 'current_level': profile.current_level})
    return JsonResponse({'status': 'error'}, status=400)
