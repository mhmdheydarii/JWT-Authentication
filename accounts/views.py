from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegistrationSerializer, LoginSerializer
# Create your views here.

class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"you`r account created",
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer