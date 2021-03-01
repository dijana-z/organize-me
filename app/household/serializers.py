from rest_framework import serializers
from core.models import Household, Grocery


class HouseholdSerializer(serializers.ModelSerializer):
    """Serializer to household object."""
    grocery_list = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Grocery.objects.all(),
        allow_null=True,
        allow_empty=True
    )
    shopping_list = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Grocery.objects.all(),
        allow_null=True,
        allow_empty=True
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
    shopping_list = GrocerySerializer(many=True, read_only=False)

    class Meta:
        model = Grocery
        fields = ('id', 'name', 'quantity')
        read_only_fields = ('id',)


class GroceryListSerializer(HouseholdSerializer):
    grocery_list = GrocerySerializer(many=True, read_only=False)

    class Meta:
        model = Grocery
        fields = ('id', 'name', 'quantity')
        read_only_fields = ('id',)
