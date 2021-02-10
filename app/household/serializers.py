from rest_framework import serializers
from core.models import Household


class HouseholdSerializer(serializers.ModelSerializer):
    """Serializer to household object."""

    class Meta:
        model = Household
        fields = ('id', 'name')
        read_only_fields = ('id',)
