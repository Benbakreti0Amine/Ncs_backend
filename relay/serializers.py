from rest_framework import serializers
from .models import RelayPoint
from users.serializers import UserSerializer

class RelayPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelayPoint
        fields = '__all__'

class RelayOperatorRegisterSerializer(UserSerializer):
    def create(self, validated_data):
        validated_data['role'] = 'RELAY_OPERATOR'
        return super().create(validated_data) 