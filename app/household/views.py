from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Household
from household import serializers


class HouseholdViewset(viewsets.ModelViewSet):
    """Viewset for the household."""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.HouseholdSerializer
    queryset = Household.objects.all()

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        users = self.request.query_params.get('users')
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', default=0))
        )
        queryset = self.queryset

        if users:
            queryset = queryset.filter(users__id__in=users)
        if assigned_only:
            queryset = queryset.filter(household__isnull=False)

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
