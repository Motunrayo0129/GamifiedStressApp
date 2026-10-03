from django.db.models import Avg, Case, IntegerField, Value, When
from django.db.models.functions import TruncWeek

from core.models import UserChallenge, Badge, UserBadge, DailyCheckIn


def award_badges(user):
    total_points = sum(userchall.challenge.points
        for userchall in UserChallenge.objects.filter(user=user, status='COMPLETED')
    )

    completed_challenges = UserChallenge.objects.filter(
        user=user, status='COMPLETED').count()

    badges = Badge.objects.filter(is_active=True)

    for badge in badges:
        if(
            badge.points_required <= total_points and
            badge.challenges_required <= completed_challenges
        ):
            UserBadge.objects.get_or_create(user=user, badge=badge)

def weekly_stress_trend(user):
    level_score = {
        "VERY_LOW": 1,
        "LOW": 2,
        "MODERATE": 3,
        "HIGH": 4,
        "VERY_HIGH": 5,
    }

    def score_expression(field_name):
        return Case(
            *[
                When(**{field_name: level, "then": Value(score)})
                for level, score in level_score.items()
            ],
            output_field=IntegerField(),
        )

    return (
        DailyCheckIn.objects.filter(user=user)
        .annotate(
            week=TruncWeek('check_in_date'),
            stress_score=score_expression("stress_level"),
            energy_score=score_expression("energy_level"),
            focus_score=score_expression("focus_level"),
        )
        .values('week')
        .annotate(
            avg_stress=Avg('stress_score'),
            avg_energy=Avg('energy_score'),
            avg_focus=Avg('focus_score'),
        )
        .order_by('week')
    )
