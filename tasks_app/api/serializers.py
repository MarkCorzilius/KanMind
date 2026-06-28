from rest_framework import serializers
from tasks_app.models import Task, Comment
from django.contrib.auth.models import User
from core.serializers import MemberSerializer

class TaskListSerializer(serializers.ModelSerializer):

    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee', queryset=User.objects.all(), allow_null=True, required=False
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer', queryset=User.objects.all(), allow_null=True, required=False
    )
    
    class Meta:
        model = Task
        fields = ['board', 'title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'due_date']


class TaskResponseSerializer(serializers.ModelSerializer):

    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    owner = MemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee', 'reviewer', 'owner', 'due_date', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()
    

class TaskUpdateSerializer(serializers.ModelSerializer):

    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee', queryset=User.objects.all(), allow_null=True, required=False
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer', queryset=User.objects.all(), allow_null=True, required=False
    )
    
    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'due_date']



class CommentsSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField(read_only=True)
    owner = MemberSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'owner', 'content']

    def get_author(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"