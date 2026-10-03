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

    class StressLevel(models.TextChoices):
        VERY_HIGH = "VERY_HIGH", "very high"
        HIGH = "HIGH", "high"
        MODERATE= "MODERATE", "moderate"
        VERY_LOW = "VERY_LOW", "very low"
        LOW = "LOW", "low"

    class EnergyLevel(models.TextChoices):
        VERY_HIGH = "VERY_HIGH", "very high"
        HIGH = "HIGH", "high"
        MODERATE = "MODERATE", "moderate"
        VERY_LOW = "VERY_LOW", "very low"
        LOW = "LOW", "low"

    class FocusLevel(models.TextChoices):
        VERY_HIGH = "VERY_HIGH", "very high"
        HIGH = "HIGH", "high"
        MODERATE = "MODERATE", "moderate"
        LOW = "LOW", "low"
        VERY_LOW = "VERY_LOW", "very low"


    check_in_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_checkins')
    check_in_date = models.DateField(auto_now_add=True)
    stress_level = models.CharField(max_length=10, choices=StressLevel.choices, default=StressLevel.MODERATE)
    energy_level = models.CharField(max_length=10, choices=EnergyLevel.choices, default=EnergyLevel.MODERATE)
    focus_level = models.CharField(max_length=10, choices=FocusLevel.choices, default=FocusLevel.MODERATE)
    mood = models.CharField(max_length=10, choices=Mood.choices, default=Mood.HAPPY)
    sleep_quality = models.CharField(max_length=10, choices=SleepQuality.choices, default=SleepQuality.POOR)

    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.check_in_date}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "check_in_date"],
                name="unique_daily_checkin_per_user",
            ),
        ]


class ChallengeCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(ChallengeCategory, on_delete=models.CASCADE, related_name='challenges')
    points = models.IntegerField(default=5, validators=[MinValueValidator(0)])
    duration = models.IntegerField(default=60, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    external_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.category.name})"

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(points__gte=0),
                name="challenge_points_nonnegative",
            ),
            models.CheckConstraint(
                condition=models.Q(duration__gt=0),
                name="challenge_duration_positive",
            ),
        ]


class SubChallenge(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='sub_challenges')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    external_link = models.URLField(blank=True, null=True)
    points = models.IntegerField(default=1, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(points__gte=0),
                name="subchallenge_points_nonnegative",
            ),
        ]


class UserChallenge(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_challenges')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='user_challenges')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='IN_PROGRESS')
    progress = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def mark_completed(self):

        from core.services import award_badges

        self.status = 'COMPLETED'
        self.progress = 100
        self.completed_at = timezone.now()
        self.save()

        award_badges(self.user)

    def update_progress(self):
        total_points = sum(
            sub.points for sub in self.challenge.sub_challenges.all()
        )

        if total_points == 0:
            self.mark_completed()
            return

        completed_points = sum(
            usc.sub_challenge.points
            for usc in self.user_sub_challenges.filter(completed=True)
        )

        self.progress = int((completed_points / total_points) * 100)

        if self.progress >= 100:
            self.mark_completed()
        else:
            self.save()

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} ({self.status})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "challenge"],
                name="unique_challenge_per_user",
            ),
            models.CheckConstraint(
                condition=models.Q(progress__gte=0) & models.Q(progress__lte=100),
                name="user_challenge_progress_range",
            ),
        ]


class UserSubChallenge(models.Model):
    user_challenge = models.ForeignKey(UserChallenge, on_delete=models.CASCADE, related_name='user_sub_challenges')
    sub_challenge = models.ForeignKey(SubChallenge, on_delete=models.CASCADE, related_name='user_sub_challenges')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def mark_completed(self):
        if not self.completed:
            self.completed = True
            self.completed_at = timezone.now()
            self.save()
            self.user_challenge.update_progress()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_challenge", "sub_challenge"],
                name="unique_subchallenge_per_user_challenge",
            ),
        ]

class Badge(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='badges/',blank=True, null=True)
    points_required = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    challenges_required = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(points_required__gte=0),
                name="badge_points_required_nonnegative",
            ),
            models.CheckConstraint(
                condition=models.Q(challenges_required__gte=0),
                name="badge_challenges_required_nonnegative",
            ),
        ]

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "badge"],
                name="unique_badge_per_user",
            ),
        ]
        ordering = ['-earned_at']

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
