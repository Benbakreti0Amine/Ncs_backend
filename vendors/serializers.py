from users.serializers import UserSerializer
from users.models import User

class VendorRegisterSerializer(UserSerializer):
    def create(self, validated_data):
        validated_data['role'] = 'VENDOR'
        return super().create(validated_data) 