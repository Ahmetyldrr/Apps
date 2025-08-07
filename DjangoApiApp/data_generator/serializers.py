from rest_framework import serializers
from .models import ForecastData

class ForecastDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForecastData
        fields = '__all__'
