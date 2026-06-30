from rest_framework import serializers
from tasks_app.models import Task, Comment
from django.contrib.auth.models import User
from core.serializers import MemberSerializer


class TaskSerializer(serializers.ModelSerializer):
    """Serialize task input data for creation, accepting assignee/reviewer by id."""

    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee', queryset=User.objects.all(), allow_null=True, required=False
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer', queryset=User.objects.all(), allow_null=True, required=False
    )
    
    class Meta:
        model = Task
        fields = ['board', 'title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'due_date']


class TaskUpdateSerializer(TaskSerializer):
    """Serialize task update data"""
    
    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'due_date']


class TaskResponseSerializer(serializers.ModelSerializer):
    """Serialize a full task response with nested user objects and comment count."""

    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    owner = MemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee', 'reviewer', 'owner', 'due_date', 'comments_count']

    def get_comments_count(self, obj):
        """Return the total number of comments on the task."""
        
        return obj.comments.count()
    

class CommentsSerializer(serializers.ModelSerializer):
    """Serialize a comment with computed author full name."""

    author = serializers.SerializerMethodField(read_only=True)
    owner = MemberSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'owner', 'content']

    def get_author(self, obj):
        """Return the comment author's full name."""

        return f"{obj.author.first_name} {obj.author.last_name}"