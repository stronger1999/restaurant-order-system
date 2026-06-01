from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, SocialLoginSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class SocialLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = SocialLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # Demo OAuth2 mode: in real deployment, verify provider access token here.
        email = data.get('email') or f"{data['provider']}_user@example.com"
        username = data.get('username') or email.split('@')[0]
        user, _ = User.objects.get_or_create(username=username, defaults={'email': email})
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'user': UserSerializer(user).data})
