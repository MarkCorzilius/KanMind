from django.db.models import Count
from boards_app.models import Board
from django.db.models import Q
from boards_app.api.serializers import BoardListSerializer, BoardCreateSerializer, BoardDetailSerializer, EmailCheckSerializer, BoardUpdateSerializer, BoardUpdateResponseSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from core.permissions import IsOwner, IsBoardMember

class BoardListCreateView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BoardCreateSerializer
        return BoardListSerializer
    
    def get_queryset(self):
        return Board.objects.filter(members=self.request.user).annotate(
            member_count=Count('members', distinct=True),
            tasks_count=Count('tasks', distinct=True),
            tasks_to_do_count=Count('tasks', filter=Q(tasks__status='to_do'), distinct=True),
            tasks_high_prio_count=Count('tasks', filter=Q(tasks__priority='high'), distinct=True)
        )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save()
        return Response(BoardDetailSerializer(board).data, status=201)
    
class BoardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    http_method_names = ['get', 'patch', 'delete']

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsOwner(), IsAuthenticated()]
        return [IsBoardMember(), IsAuthenticated()]
    
    def partial_update(self, request, *args, **kwargs):
        board = self.get_object()
        serializer = BoardUpdateSerializer(board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        board = serializer.save()
        return Response(BoardUpdateResponseSerializer(board).data)

    
class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailCheckSerializer

    def get(self, request):
        email = request.query_params.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist.'}, status=404)
        return Response(EmailCheckSerializer(user).data)
