from django.contrib import admin

from core.models import DailyCheckIn, ChallengeCategory, Challenge, SubChallenge, UserChallenge, UserSubChallenge, \
    Badge, UserBadge


# Register your models here.

@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = ('user', 'check_in_date', 'stress_level', 'mood')
    list_filter = ('mood', 'sleep_quality', 'is_active')
    search_fields = ('user__username', 'notes')

@admin.register(ChallengeCategory)
class ChallengeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'points', 'duration', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description')

@admin.register(SubChallenge)
class SubChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'challenge', 'points')
    search_fields = ('title', 'description')

@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'status', 'progress', 'completed_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'notes')

@admin.register(UserSubChallenge)
class UserSubChallengeAdmin(admin.ModelAdmin):
    list_display = ('user_challenge', 'sub_challenge', 'completed', 'completed_at')
    list_filter = ('completed',)

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('badge', 'user', 'earned_at')