from rest_framework import generics
from tasks_app.models import Task
from core.permissions import IsBoardMember, IsOwner
from tasks_app.api.permissions import IsTaskBoardMember
from tasks_app.api.permissions import IsTaskAssignee
from rest_framework.permissions import IsAuthenticated
from tasks_app.api.serializers import TaskListSerializer, TaskResponseSerializer, TaskUpdateSerializer
from rest_framework.response import Response

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsBoardMember, IsAuthenticated]
    serializer_class = TaskListSerializer

    def create(self, request, *args, **kwargs):
        serializer = TaskListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(owner=request.user)
        return Response(TaskResponseSerializer(task).data)


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



class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    http_method_names = ['patch', 'delete']

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [(IsOwner | IsTaskAssignee)(), IsAuthenticated()]
        return [IsTaskBoardMember(), IsAuthenticated()]
    
    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(TaskResponseSerializer(task).data)


# if reviewer or assignee is not in board = unset