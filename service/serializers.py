from rest_framework import serializers
from . import models


class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Building
        fields = ['id', 'point']


class PolySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Building
        fields = ['id', 'polygon', 'business_type', 'rank', 'fill']