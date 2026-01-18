import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import User


class DailyCheckIn(models.Model):
    class Mood(models.TextChoices):
        HAPPY = "HAPPY", "happy"
        NEUTRAL = "NEUTRAL", "neutral"
        SAD = "SAD", "sad"
        ANXIOUS = "ANXIOUS", "anxious"

    class SleepQuality(models.TextChoices):
        POOR = "POOR", "poor"
        FAIR = "FAIR", "fair"
        GOOD = "GOOD", "good"

    check_in_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_checkins')
    check_in_date = models.DateField(auto_now_add=True)

    stress_level = models.IntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    energy_level = models.IntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    focus_level = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])

    mood = models.CharField(max_length=10, choices=Mood.choices, default=Mood.HAPPY)
    sleep_quality = models.CharField(max_length=10, choices=SleepQuality.choices, default=SleepQuality.POOR)

    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.check_in_date}"


class ChallengeCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(ChallengeCategory, on_delete=models.CASCADE, related_name='challenges')
    points = models.IntegerField(default=5)
    duration = models.IntegerField(default=60)
    is_active = models.BooleanField(default=True)
    external_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.category.name})"


class SubChallenge(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='sub_challenges')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    external_link = models.URLField(blank=True, null=True)
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class UserChallenge(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_challenges')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='user_challenges')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='IN_PROGRESS')
    progress = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def mark_completed(self):
        self.status = 'COMPLETED'
        self.progress = 100
        self.completed_at = timezone.now()
        self.save()


class UserSubChallenge(models.Model):
    user_challenge = models.ForeignKey(UserChallenge, on_delete=models.CASCADE, related_name='user_sub_challenges')
    sub_challenge = models.ForeignKey(SubChallenge, on_delete=models.CASCADE, related_name='user_sub_challenges')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
