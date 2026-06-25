from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'repeated_password']

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        
        parts = data['fullname'].split(' ', 1)
        if len(parts) < 2:
            raise serializers.ValidationError({'fullname': 'First and last name required.'})
        data['first_name'] = parts[0]
        data['last_name'] = parts[1]

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists.'})

        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')

        return User.objects.create_user(
            username = validated_data['email'],
            email = validated_data['email'],
            password = validated_data['password'],
            first_name  = validated_data['first_name'],
            last_name = validated_data['last_name']
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