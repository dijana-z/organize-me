from rest_framework import serializers
from core.models import Household, Grocery


class HouseholdSerializer(serializers.ModelSerializer):
    """Serializer to household object."""
    grocery_list = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Grocery.objects.all()
    )
    shopping_list = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Grocery.objects.all()
    )

    class Meta:
        model = Household
        fields = ('id', 'name', 'grocery_list', 'shopping_list')
        read_only_fields = ('id',)


class GrocerySerializer(serializers.ModelSerializer):
    """Serializer to grocery object."""

    class Meta:
        model = Grocery
        fields = ('id', 'name', 'quantity')
        read_only_fields = ('id',)


class ShoppingListSerializer(HouseholdSerializer):
    shopping = GrocerySerializer(many=True, read_only=False)


class GroceryListSerializer(HouseholdSerializer):
    groceries = GrocerySerializer(many=True, read_only=False)
