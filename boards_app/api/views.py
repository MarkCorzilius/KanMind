from django.db.models import Count
from boards_app.models import Board
from django.db.models import Q
from boards_app.api.serializers import BoardListSerializer, BoardCreateSerializer, \
    BoardDetailSerializer, BoardUpdateSerializer, BoardUpdateResponseSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.permissions import IsOwner, IsBoardMember


class BoardListCreateView(generics.ListCreateAPIView):
    """List all boards for the current user or create a new board."""
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated]

    def annotate_tasks(self, qs):
        """Adds task statistics (total, to-do, high priority) to a queryset."""
        return qs.annotate(
            ticket_count=Count('tasks', distinct=True),
            tasks_to_do_count=Count('tasks', filter=Q(tasks__status='to-do'), distinct=True),
            tasks_high_prio_count=Count('tasks', filter=Q(tasks__priority='high'), distinct=True)
        )

    def get_serializer_class(self):
        """Chooses create or list serializer based on request method."""
        if self.request.method == 'POST':
            return BoardCreateSerializer
        return BoardListSerializer
    
    def get_queryset(self):
        """Returns the user’s boards with annotated task counts."""
        return self.annotate_tasks(Board.objects.filter(members=self.request.user))
    
    def create(self, request, *args, **kwargs):
        """Creates a board and returns it with annotated task counts."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save()
        annotated = self.annotate_tasks(Board.objects.filter(pk=board.pk)).first()
        return Response(BoardListSerializer(annotated).data, status=201)
    
    
class BoardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, partially update, or delete a single board."""
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    http_method_names = ['get', 'patch', 'delete']

    def get_permissions(self):
        """Require ownership for DELETE; board membership for all other methods."""
        if self.request.method == 'DELETE':
            return [IsOwner(), IsAuthenticated()]
        return [IsBoardMember(), IsAuthenticated()]
    
    def partial_update(self, request, *args, **kwargs):
        """Partially update a board and return the updated response data."""
        board = self.get_object()
        serializer = BoardUpdateSerializer(board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        board = serializer.save()
        return Response(BoardUpdateResponseSerializer(board).data)