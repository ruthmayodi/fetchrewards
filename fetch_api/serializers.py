from rest_framework import serializers 
from .models import Points


class PointsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Points
        fields = [
            'id',
            'payer',
            'points',
            'timestamp',
        ]


class TotalPointsSerializer(serializers.HyperlinkedModelSerializer):
    total_points = serializers.IntegerField()
    class Meta:
        model = Points
        fields = [
            'id',
            'payer',
            'total_points',
        ]
