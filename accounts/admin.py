#accounts/admin.py

from django.contrib import admin
from .models import School, StudentProfile, TeacherProfile

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'year', 'points', 'current_level', 'is_active')
    search_fields = ('user__username', 'school__name')

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'is_school_admin')
    search_fields = ('user__username', 'school__name')
