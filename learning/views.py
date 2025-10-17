from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Level, Quiz, Question, Choice
from accounts.models import StudentProfile, TeacherProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# ---------------- HOME ---------------- #
def home_redirect(request):
    leaves = range(10)  # 10 leaves
    return render(request, "home.html", {"leaves": leaves})


def home_redirect(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser:
            return redirect('/admin/')
        if hasattr(user, 'teacher_profile') and user.teacher_profile.is_school_admin:
            return redirect('teacher_dashboard')
        if hasattr(user, 'student_profile'):
            return redirect('student_dashboard')
    return render(request, 'home.html')


# ---------------- STUDENT DASHBOARD ---------------- #
@login_required
def student_dashboard(request):
    profile = getattr(request.user, 'student_profile', None)
    levels = Level.objects.order_by('number')

    return render(request, 'learning/student_dashboard.html', {
        'profile': profile,
        'levels': levels,
    })


@login_required
def level_view(request, number):
    level = get_object_or_404(Level, number=number)
    profile = getattr(request.user, 'student_profile', None)

    # Prevent accessing future levels
    if profile.current_level < level.number:
        messages.warning(request, "You must complete previous levels first.")
        return redirect('student_dashboard')

    # Handle level completion via AJAX
    if request.method == 'POST':
        profile.complete_level(level)
        return JsonResponse({'status': 'ok', 'points': profile.points, 'current_level': profile.current_level})

    # Prepare quiz questions for template
    # Example structure: list of dicts
    quiz_questions = []
    for quiz in level.quizzes.all():
        for q in quiz.questions.all():
            quiz_questions.append({
                'question': q.text,
                'options': [c.text for c in q.choices.all()],
                'answer': q.choices.get(is_correct=True).text,
                'explanation': q.explanation
            })

    context = {
        'level': level,
        'profile': profile,
        'video_src': level.video_file.url if level.video_file else '',  # video uploaded for this level
        'quiz_questions': json.dumps(quiz_questions)  # pass as JSON
    }
    return render(request, f'learning/level{number}.html', context)



# ---------------- TEACHER DASHBOARD ---------------- #
@login_required
def teacher_dashboard(request):
    tp = getattr(request.user, 'teacher_profile', None)
    if not tp or not tp.is_school_admin:
        messages.error(request, 'Not authorized')
        return redirect('login')

    students = tp.school.students.filter(is_active=True).order_by('-points')
    return render(request, 'learning/teacher_dashboard.html', {'students': students})


# ---------------- COMPLETE LEVEL (Direct URL access) ---------------- #
@login_required
def complete_level(request, number):
    profile = getattr(request.user, 'student_profile', None)
    if not profile:
        messages.error(request, "No student profile found.")
        return redirect('student_dashboard')

    level = get_object_or_404(Level, number=number)

    # Only allow completing current level
    if profile.current_level == level.number:
        if level not in profile.completed_levels.all():
            profile.complete_level(level)
            messages.success(request, f"You completed {level.title} and earned 100 points!")
        else:
            messages.info(request, "This level is already completed.")
    else:
        messages.warning(request, "You cannot complete this level yet.")

    return redirect('student_dashboard')


# ---------------- AWARD POINTS (AJAX Support) ---------------- #
@login_required
@csrf_exempt
def award_points(request):
    if request.method == 'POST':
        profile = getattr(request.user, 'student_profile', None)
        if not profile:
            return JsonResponse({'status': 'error', 'message': 'No student profile'}, status=400)
        try:
            points_earned = int(request.POST.get('points', 0))
        except ValueError:
            points_earned = 0

        profile.add_points(points_earned)
        return JsonResponse({
            'status': 'ok',
            'points': profile.points,
            'current_level': profile.current_level
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
