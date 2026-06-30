from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core import exceptions
from .models import User, Profile


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
    

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField()
    new_password = serializers.CharField()
    complete_password = serializers.CharField()

    def validate(self, attrs):
        if attrs["new_password"] != attrs["complete_password"]:
            raise serializers.ValidationError({"message":"password didn`t match"})
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"data":[e.messages]})
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["email" ,"first_name", "last_name", "created_date"]