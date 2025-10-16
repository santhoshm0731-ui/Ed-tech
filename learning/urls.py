from django.urls import path
from . import views

# learning/urls.py
urlpatterns = [
    path('', views.home_view, name='home'),  # root now shows home.html
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('level/1/', views.level1_view, name='level1'),
    path('level/2/', views.level2_view, name='level2'),
    path('api/award_points/', views.award_points, name='award_points'),
]


