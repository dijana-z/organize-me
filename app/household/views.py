from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Household, Grocery
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


class GroceryViewSet(viewsets.ModelViewSet):
    """Viewset for grocery item."""
    queryset = Grocery.objects.all()
    serializer_class = serializers.GrocerySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class GroceryListViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.GroceryListSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        household = self.request.user.household
        return self.queryset.filter(household=household).\
            orderby('-name').distinct()


class ShoppingListViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ShoppingListSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        household = self.request.user.household
        return self.queryset.filter(household=household).\
            orderby('-name').distinct()
