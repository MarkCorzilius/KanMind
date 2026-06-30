from rest_framework import generics
from tasks_app.models import Task, Comment
from core.permissions import IsBoardMember, IsOwner
from tasks_app.api.permissions import IsTaskBoardMember, IsCommentAuthor
from tasks_app.api.permissions import IsTaskAssignee, IsCommentBoardMember
from rest_framework.permissions import IsAuthenticated
from tasks_app.api.serializers import TaskSerializer, TaskResponseSerializer, TaskUpdateSerializer, CommentsSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from boards_app.models import Board


class TaskCreateView(generics.CreateAPIView):
    """Create a new task on a board."""
    
    queryset = Task.objects.all()
    permission_classes = [IsTaskBoardMember, IsAuthenticated]
    serializer_class = TaskSerializer

    def get_task(self):
        return get_object_or_404(Task, pk=self.kwargs["task_pk"])

    def create(self, request, *args, **kwargs):
        """Create a task with the current user as owner and return the full task response."""

        board = get_object_or_404(Board, pk=request.data['board'])
        if not board.members.filter(id=request.user.id).exists():
            raise PermissionDenied('You are not a member of this board')

        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(owner=request.user)
        return Response(TaskResponseSerializer(task).data, status=201)


class TasksAssignedToCurrentUserView(generics.ListAPIView):
    """List all tasks assigned to the current user."""

    queryset = Task.objects.all()
    permission_classes = [IsBoardMember, IsAuthenticated]
    serializer_class = TaskResponseSerializer

    def get_queryset(self):
        """Return all tasks assigned to the current user."""
        return Task.objects.filter(assignee=self.request.user, board__members=self.request.user)


class TasksReviewByCurrentUserView(generics.ListAPIView):
    """List all tasks where the current user is the reviewer."""

    queryset = Task.objects.all()
    permission_classes = [IsBoardMember, IsAuthenticated]
    serializer_class = TaskResponseSerializer

    def get_queryset(self):
        """Return all tasks where the current user is the reviewer."""
        return Task.objects.filter(reviewer=self.request.user, board__members=self.request.user)


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Partially update or delete a single task."""

    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_pk'
    http_method_names = ['patch', 'delete']
    serializer_class = TaskUpdateSerializer

    def get_permissions(self):
        """Require ownership or assignee status for DELETE; board membership otherwise."""
        if self.request.method == 'DELETE':
            return [(IsOwner | IsTaskAssignee)(), IsAuthenticated()]
        return [IsTaskBoardMember(), IsAuthenticated()]
    
    def partial_update(self, request, *args, **kwargs):
        """Partially update a task and return the full task response."""

        task = self.get_object()
        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(TaskResponseSerializer(task).data)


class CommentsListCreateViewSet(viewsets.ModelViewSet):
    """List, create, and delete comments on a task."""

    queryset = Comment.objects.all()
    http_method_names = ['get', 'post', 'delete']
    serializer_class = CommentsSerializer

    def get_task(self):
        return get_object_or_404(Task, pk=self.kwargs["task_pk"])


    def get_permissions(self):
        """Require comment authorship for DELETE; board membership for other methods."""

        if self.request.method == "DELETE":
            return [IsCommentAuthor()]
        return [IsCommentBoardMember()]

    def get_queryset(self):
        task = self.get_task()
        return Comment.objects.filter(task=task)
    
    def create(self, request, *args, **kwargs):
        """Create a comment on the task, set the current user as author."""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = self.get_task()
        comment = serializer.save(author=request.user, task=task)
        return Response(CommentsSerializer(comment).data, status=201)

