from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'nom', 'prenom', 
                 'numero_de_telephone',  'is_active', 'is_staff', 'role']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'nom': {'required': True},
            'prenom': {'required': True},
            'numero_de_telephone': {'required': True}
        }

    def validate(self, attrs):
        numero_de_telephone = attrs.get("numero_de_telephone")

        if numero_de_telephone and User.objects.filter(numero_de_telephone=numero_de_telephone).exists():
            raise ValidationError("Phone number has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        print(user.is_staff)
        print(user.role)
        print(user.is_active)
        return user



# from rest_framework import serializers
# from rest_framework.validators import ValidationError
# from django.utils.http import urlsafe_base64_decode
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'password', 'nom', 'prenom', 'matricule_de_voiture', 'numero_de_telephone', 'latitude', 'longitude', 'is_active']
#         extra_kwargs = {'password': {'write_only': True}}

#     def validate(self, attrs):
#         email = attrs.get("email")
#         numero_de_telephone = attrs.get("numero_de_telephone")

#         if email and User.objects.filter(email=email).exists():
#             raise ValidationError("Email has already been used")

#         if numero_de_telephone and User.objects.filter(numero_de_telephone=numero_de_telephone).exists():
#             raise ValidationError("Phone number has already been used")

#         return super().validate(attrs)

#     def create(self, validated_data):
#         password = validated_data.pop("password")
#         user = User.objects.create_user(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user

# class ResetPasswordEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)

# class ResetPasswordSerializer(serializers.Serializer):
#     new_password = serializers.CharField(write_only=True, min_length=1)

#     class Meta:
#         fields = ("new_password",)

#     def validate(self, data):
#         password = data.get("new_password")
#         token = self.context.get("kwargs").get("token")
#         encoded_pk = self.context.get("kwargs").get("encoded_pk")

#         if token is None or encoded_pk is None:
#             raise serializers.ValidationError("Missing data.")

#         pk = urlsafe_base64_decode(encoded_pk).decode()
#         user = User.objects.get(pk=pk)
#         if not PasswordResetTokenGenerator().check_token(user, token):
#             raise serializers.ValidationError("The reset token is invalid")

#         user.set_password(password)
#         user.save()
#         return data

# class NewPasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)

