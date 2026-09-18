from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class MemberSerializer(serializers.ModelSerializer):
    """Serialize a User to id, email, and computed full name."""

    fullname = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']
    
    def get_fullname(self, obj):
        """Return the user's full name as 'first last'."""
        return f"{obj.first_name} {obj.last_name}"
    