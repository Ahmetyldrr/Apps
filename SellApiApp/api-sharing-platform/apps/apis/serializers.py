from rest_framework import serializers
from .models import Api

class ApiSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Api
        fields = ['id', 'user', 'name', 'description', 'endpoint', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']