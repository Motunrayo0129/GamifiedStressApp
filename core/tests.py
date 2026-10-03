from datetime import timedelta

from django.db import IntegrityError, transaction
from django.test import TestCase

from core.models import Badge, Challenge, ChallengeCategory, DailyCheckIn, UserChallenge
from core.serializers import DailyCheckInSerializer
from core.services import award_badges, weekly_stress_trend
from user.models import User


class DailyCheckInTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="checkin-user",
            email="checkin@example.com",
            password="test-password",
        )

    def test_serializer_exposes_focus_level(self):
        self.assertIn("focus_level", DailyCheckInSerializer().fields)

    def test_user_can_have_only_one_checkin_per_day(self):
        DailyCheckIn.objects.create(user=self.user)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                DailyCheckIn.objects.create(user=self.user)

    def test_weekly_analytics_maps_text_levels_to_scores(self):
        first = DailyCheckIn.objects.create(
            user=self.user,
            stress_level=DailyCheckIn.StressLevel.HIGH,
            energy_level=DailyCheckIn.EnergyLevel.LOW,
            focus_level=DailyCheckIn.FocusLevel.MODERATE,
        )
        second = DailyCheckIn.objects.create(
            user=User.objects.create_user(
                username="other-user",
                email="other@example.com",
                password="test-password",
            ),
        )
        second.user = self.user
        second.check_in_date = first.check_in_date - timedelta(days=7)
        second.stress_level = DailyCheckIn.StressLevel.LOW
        second.energy_level = DailyCheckIn.EnergyLevel.VERY_HIGH
        second.focus_level = DailyCheckIn.FocusLevel.HIGH
        second.save(update_fields=["user", "check_in_date", "stress_level", "energy_level", "focus_level"])

        trends = list(weekly_stress_trend(self.user))

        self.assertEqual(len(trends), 2)
        self.assertEqual({trend["avg_stress"] for trend in trends}, {2.0, 4.0})
        self.assertEqual({trend["avg_energy"] for trend in trends}, {2.0, 5.0})
        self.assertEqual({trend["avg_focus"] for trend in trends}, {3.0, 4.0})


class BadgeTests(TestCase):
    def test_badge_is_awarded_when_points_threshold_is_reached(self):
        user = User.objects.create_user(
            username="badge-user",
            email="badge@example.com",
            password="test-password",
        )
        category = ChallengeCategory.objects.create(name="Mindfulness")
        challenge = Challenge.objects.create(
            title="Take a break",
            category=category,
            points=5,
        )
        UserChallenge.objects.create(
            user=user,
            challenge=challenge,
            status="COMPLETED",
            progress=100,
        )
        badge = Badge.objects.create(name="First step", points_required=5)

        award_badges(user)

        self.assertTrue(badge.user_badges.filter(user=user).exists())
