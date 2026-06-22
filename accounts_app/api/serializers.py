from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(source="username")

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'repeated_password']

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data
        
    def create(self, validated_data):
        validated_data.pop('repeated_password')

        return User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        if not user or not user.check_password(attrs['password']):
            raise serializers.ValidationError('Invalid credentials.')
        attrs['user'] = user
        return attrs