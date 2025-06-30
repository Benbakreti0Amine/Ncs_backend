from rest_framework import serializers
from .models import EmploymentPost, RelayApplication

class EmploymentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentPost
        fields = '__all__'

class RelayApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelayApplication
        fields = '__all__' 