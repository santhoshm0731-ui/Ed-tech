from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.student_signup_view, name='signup'),
    path('teacher-signup/', views.teacher_signup_view, name='teacher_signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
