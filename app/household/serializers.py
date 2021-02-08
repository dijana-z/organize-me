from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import Household


class HouseholdSerializer(serializers.ModelSerializer):
    """Serializer to household object."""
    users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Household
        fields = ('id', 'name')
        read_only_fields = ('id',)
