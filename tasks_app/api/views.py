from rest_framework import generics
from tasks_app.models import Task, Comment
from core.permissions import IsBoardMember, IsOwner
from tasks_app.api.permissions import IsTaskBoardMember, IsCommentAuthor
from tasks_app.api.permissions import IsTaskAssignee, IsCommentBoardMember
from rest_framework.permissions import IsAuthenticated
from tasks_app.api.serializers import TaskListSerializer, TaskResponseSerializer, TaskUpdateSerializer, CommentsSerializer
from rest_framework.response import Response
from rest_framework import viewsets

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
    serializer_class = TaskResponseSerializer

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)


class TasksReviewByCurrentUserView(generics.ListAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsBoardMember, IsAuthenticated]
    serializer_class = TaskResponseSerializer

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)



class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_pk'
    http_method_names = ['patch', 'delete']
    serializer_class = TaskUpdateSerializer

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



class CommentsListCreateViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    http_method_names = ['get', 'post', 'delete']
    serializer_class = CommentsSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsCommentAuthor(), IsAuthenticated()]
        return [IsCommentBoardMember(), IsAuthenticated()]

    def list(self, request, task_pk=None):
        comments = Comment.objects.filter(task=task_pk)
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(author=request.user, task_id=self.kwargs['task_pk'])
        return Response(CommentsSerializer(comment).data)
    
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response(status=204)

