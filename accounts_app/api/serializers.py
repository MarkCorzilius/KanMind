from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Validate and create a new user account."""

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'repeated_password']

    def validate(self, data):
        """Validate passwords match, fullname has two parts, and email is unique."""
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
        """Create and return a new user from validated data."""
        validated_data.pop('repeated_password')

        return User.objects.create_user(
            username = validated_data['email'],
            email = validated_data['email'],
            password = validated_data['password'],
            first_name  = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
    

class LoginSerializer(serializers.Serializer):
    """Validate user credentials and expose the authenticated user."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Validate credentials and attach the user to the returned data."""
        user = User.objects.filter(email=attrs['email']).first()
        if not user or not user.check_password(attrs['password']):
            raise serializers.ValidationError('Invalid credentials.')
        attrs['user'] = user
        return attrs
    

class EmailCheckSerializer(serializers.ModelSerializer):
    """Serialize a user for the email-check lookup endpoint."""

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        """Return the user's full name as 'first last'."""
        return f"{obj.first_name} {obj.last_name}"
    
