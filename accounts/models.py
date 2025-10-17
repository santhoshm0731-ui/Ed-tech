from django.db import models
from django.contrib.auth.models import User
from learning.models import Level

class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    year = models.PositiveIntegerField(null=True, blank=True)
    school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    points = models.IntegerField(default=0)
    current_level = models.PositiveIntegerField(default=1)
    completed_levels = models.ManyToManyField('learning.Level', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} ({self.school})" if self.school else self.user.username

    def add_points(self, earned_points):
        """Simply add points, no automatic unlocking here."""
        self.points += earned_points
        self.save()

    def complete_level(self, level):
        """Mark level as completed and unlock next level."""
        if level not in self.completed_levels.all():
            self.completed_levels.add(level)
            self.add_points(100)  # ✅ +100 points only once per level

            # Unlock next level
            if self.current_level == level.number:
                self.current_level += 1

            self.save()

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    school = models.OneToOneField(School, on_delete=models.SET_NULL, null=True, blank=True, related_name='teacher')
    is_school_admin = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.school}"
