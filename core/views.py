from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from core.models import DailyCheckIn, ChallengeCategory, Challenge, SubChallenge, UserChallenge, UserSubChallenge
from core.serializers import DailyCheckInSerializer, ChallengeCategorySerializer, ChallengeSerializer, \
    SubChallengeSerializer, UserChallengeSerializer, UserSubChallengeSerializer


# Create your views here.

class DailyCheckInViewSet(viewsets.ModelViewSet):
    serializer_class = DailyCheckInSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DailyCheckIn.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChallengeCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChallengeCategory.objects.all()
    serializer_class = ChallengeCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Challenge.objects.filter(is_active=True)

class SubChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = SubChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SubChallenge.objects.filter(challenge__is_active=True)

class UserChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = UserChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserChallenge.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.data.get("status") == "COMPLETED":
            instance.mark_complete()

        return super().partial_update(request, *args, **kwargs)

class UserSubChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSubChallenge.objects.filter(
            user_challenge__user=self.request.user
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.data.get("status") == "completed":
            instance.mark_complete()
            instance.save()

        return Response(
            self.get_serializer(instance).data,
            status=status.HTTP_200_OK
        )