from rest_framework import serializers
from boards_app.models import Board
from django.contrib.auth.models import User
from core.serializers import MemberSerializer
from tasks_app.api.serializers import TaskResponseSerializer

class BoardListSerializer(serializers.ModelSerializer):

    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.IntegerField(read_only=True)
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()



class BoardCreateSerializer(serializers.ModelSerializer):

    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    
    class Meta:
        model = Board
        fields = ['title', 'members']

    def create(self, validated_data):
        members = validated_data.pop('members')
        owner = self.context['request'].user
        board = Board.objects.create(owner=owner, **validated_data)
        board.members.set(members)
        board.members.add(owner)
        return board
    

class BoardUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ['title', 'members']



class BoardUpdateResponseSerializer(serializers.ModelSerializer):

    owner_data = MemberSerializer(source='owner' ,read_only=True)
    members_data = MemberSerializer(source='members', many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_data', 'members_data']

    

class BoardDetailSerializer(serializers.ModelSerializer):

    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    members = MemberSerializer(many=True, read_only=True)
    tasks = TaskResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']
        

class EmailCheckSerializer(serializers.ModelSerializer):

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
