#learning/admin.py

from django.contrib import admin
from .models import Level, Quiz, Question, Choice

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'required_points')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'level')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
