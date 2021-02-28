from rest_framework import viewsets, mixins, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Household, Grocery
from household import serializers


class HouseholdViewset(viewsets.ModelViewSet, viewsets.GenericViewSet):
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


class GroceryViewSet(viewsets.ModelViewSet):
    """Viewset for grocery item."""
    queryset = Grocery.objects.all()
    serializer_class = serializers.GrocerySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Save grocery in user household."""
        serializer.save(household=self.request.user.household)

    def get_queryset(self):
        """Return only groceries in user household."""
        household = self.request.user.household
        return self.queryset.filter(household=household)


class GroceryListViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.GroceryListSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        household = self.request.user.household
        queryset = Household.objects.filter(name=household.name)
        return queryset[0].grocery_list

    def perform_create(self, serializer):
        """Create a new item in grocery list."""
        household = Household.objects.filter(
            name=self.request.user.household.name)[0]
        grocery = Grocery.objects.create(**serializer.validated_data,
                                         household=household)
        household.grocery_list.add(grocery)
        household.save()
        serializer.save(household=self.request.user.household)


class ShoppingListViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ShoppingListSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        household = self.request.user.household
        queryset = Household.objects.filter(name=household.name)
        return queryset[0].shopping_list

    def perform_create(self, serializer):
        """Create a new item in shopping list."""
        household = Household.objects.filter(
            name=self.request.user.household.name)[0]
        grocery = Grocery.objects.create(**serializer.validated_data,
                                         household=household)
        household.shopping_list.add(grocery)
        household.save()
        serializer.save(household=self.request.user.household)
