from django.db.models import Avg
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
    return (
        DailyCheckIn.objects.filter(user=user)
        .annotate(week=TruncWeek('check_in_date'))
        .values('week')
        .annotate(
            avg_stress=Avg('stress_level'),
            avg_energy=Avg('energy_level'),
            avg_focus=Avg('focus_level'),

                  )
        .order_by('week')
    )