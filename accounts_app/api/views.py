from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from accounts_app.api.serializers import RegisterSerializer, LoginSerializer, EmailCheckSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class RegisterView(APIView):
    """Handle user registration requests."""

    permission_classes = [AllowAny]
    def post(self, request):
        """Register a new user and return their token and profile info."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "fullname": f"{user.first_name} {user.last_name}",
                "email": user.email,
                "user_id": user.id,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Handle user login and token retrieval."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticate a user and return their token and profile info."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'fullname': f"{user.first_name} {user.last_name}",
            'email': user.email,
            'user_id': user.id,
        }, status=status.HTTP_200_OK)
    

class EmailCheckView(APIView):
    """Look up a user by email address."""

    permission_classes = [IsAuthenticated]
    serializer_class = EmailCheckSerializer
    http_method_names = ['get']

    def get(self, request):
        """Look up a user by email query param and return their id, email, and fullname."""
        email = request.query_params.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist.'}, status=404)
        return Response(EmailCheckSerializer(user).data)
