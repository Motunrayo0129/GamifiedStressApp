from rest_framework import serializers
from core.models import (
    DailyCheckIn, ChallengeCategory, Challenge,
    SubChallenge, UserChallenge, UserSubChallenge, Badge, UserBadge
)


class DailyCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyCheckIn
        fields = [
            'check_in_id', 'check_in_date', 'stress_level',
            'energy_level', 'focus_level', 'mood',
            'sleep_quality', 'notes', 'is_active'
        ]
        read_only_fields = ['check_in_id', 'check_in_date']


class ChallengeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeCategory
        fields = ['id', 'name', 'description']


class SubChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubChallenge
        fields = ['id', 'title', 'description', 'external_link', 'points']


class ChallengeSerializer(serializers.ModelSerializer):
    category = ChallengeCategorySerializer(read_only=True)
    sub_challenges = SubChallengeSerializer(many=True, read_only=True)

    class Meta:
        model = Challenge
        fields = [
            'id', 'title', 'description', 'category',
            'external_link', 'points', 'is_active',
            'sub_challenges'
        ]


class UserSubChallengeSerializer(serializers.ModelSerializer):
    sub_challenge = SubChallengeSerializer(read_only=True)

    class Meta:
        model = UserSubChallenge
        fields = ['id', 'sub_challenge', 'completed', 'completed_at']


class UserChallengeSerializer(serializers.ModelSerializer):
    challenge = ChallengeSerializer(read_only=True)
    user_sub_challenges = UserSubChallengeSerializer(many=True, read_only=True)

    class Meta:
        model = UserChallenge
        fields = [
            'id', 'challenge', 'status',
            'progress', 'notes',
            'completed_at', 'user_sub_challenges'
        ]

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = [
            'id', 'name', 'description', 'icon',
            'points','is_active'
        ]

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    class Meta:
        model = UserBadge
        fields = [
            'id', 'earned_at', 'badge',
        ]