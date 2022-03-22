from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Profile
from .serializers import RegisterSerializer, \
    MyTokenObtainPairSerializer, ProfileSerializer, \
    ProfileSerializerGet
from rest_framework import generics, status


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProfileViewPost(generics.CreateAPIView):
    queryset = Profile.objects
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication, )

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        data._mutable = True
        data['user'] = user.id
        serializer = ProfileSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewGet(generics.UpdateAPIView):
    serializer_class = ProfileSerializerGet
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication, )
    queryset = Profile.objects
    lookup_field = 'user_id'


