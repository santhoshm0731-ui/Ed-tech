from django.urls import path
from . import views

urlpatterns = [
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # Level view
    path('level/<int:number>/', views.level_view, name='level_view'),

    # Level completion
    path('level/<int:number>/complete/', views.complete_level, name='complete_level'),
]
