from django.contrib import admin
from .models import Level, Quiz

class LevelAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'required_points')  # make sure 'required_points' exists in Level model

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'level')

admin.site.register(Level, LevelAdmin)
admin.site.register(Quiz, QuizAdmin)
