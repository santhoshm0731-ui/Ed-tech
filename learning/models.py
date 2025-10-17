from django.db import models

# models.py
from django.db import models

class Level(models.Model):
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)

    def required_points(self):
        return self.number * 100

    def __str__(self):
        return f"Level {self.number} - {self.title}"


class Quiz(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    explanation = models.TextField(blank=True)

    def __str__(self):
        return self.text[:50]

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
