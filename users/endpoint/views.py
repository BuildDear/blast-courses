from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserRegistrationSerializer


# Own REGISTRATION
class RegistrationView(APIView):
    """Custom user registration"""

    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        user = request.data.get("user", {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Own LOGIN
class LoginAPIView(APIView):
    """Custom login view"""

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get("user", {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

