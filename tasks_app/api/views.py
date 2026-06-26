from rest_framework import generics
from rest_framework.views import APIView
from tasks_app.models import Task
from core.permissions import IsBoardMember, IsOwner
from rest_framework.permissions import IsAuthenticated
from tasks_app.api.serializers import TaskListSerializer, TaskListResponseSerializer
from rest_framework.response import Response

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsBoardMember, IsAuthenticated]
    serializer_class = TaskListSerializer

    def create(self, request, *args, **kwargs):
        serializer = TaskListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(TaskListResponseSerializer(task).data)


class TasksAssignedToCurrentUserView(generics.ListAPIView):

    queryset = Task.objects.all()
    permission_classes = [IsBoardMember, IsAuthenticated]
    serializer_class = TaskListSerializer

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)



class TasksReviewByCurrentUserView(generics.ListAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsBoardMember, IsAuthenticated]
    serializer_class = TaskListSerializer

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)