from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from django.core import exceptions

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"Password":"Password didn`t match"})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"message":[e.messages]})
        return super().validate(attrs)
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data["email"],
            password = validated_data["password"] 
        )
        return user


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data["email"] = self.user.email

        return validated_data

