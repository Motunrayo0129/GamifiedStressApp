from rest_framework import routers

from . import views

from core.views import UserSubChallengeViewSet, DailyCheckInViewSet

router = routers.DefaultRouter()

router.register('daily-checkins', views.DailyCheckInViewSet, basename='daily-checkins')
router.register('challenges', views.ChallengeViewSet, basename='challenges')
router.register('challenge-categories', views.ChallengeCategoryViewSet, basename='challenge-categories')
router.register('sub-challenges', views.SubChallengeViewSet, basename='sub-challenges')
router.register('user-challenges', views.UserChallengeViewSet, basename='user-challenges')
router.register('user-sub-challenges', views.UserSubChallengeViewSet, basename='user-sub-challenges')
router.register('badges', views.BadgeViewSet, basename='badges')
router.register('user-badges', views.UserBadgeViewSet, basename='user-badges')

urlpatterns = router.urls



