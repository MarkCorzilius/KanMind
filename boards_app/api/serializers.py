from rest_framework import serializers
from boards_app.models import Board
from django.contrib.auth.models import User

class BoardListSerializer(serializers.ModelSerializer):

    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    tickets_count = serializers.IntegerField(read_only=True)
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'tickets_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']



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
    

class BoardDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = '__all__'


class EmailCheckSerializer(serializers.ModelSerializer):

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}"