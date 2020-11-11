from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView


class AnonymousAPIView(APIView):
    permission_classes = [permissions.AllowAny]


class LoginRequiredAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]


class TokenAuthMixin(LoginRequiredAPIView):
    authentication_classes = [TokenAuthentication]
