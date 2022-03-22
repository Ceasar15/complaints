from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Profile
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer, ProfileSerializer
from rest_framework import generics


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProfileView(generics.ListCreateAPIView):
    queryset = Profile.objects
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication, )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        return self.queryset.get(user=self.request.user)

