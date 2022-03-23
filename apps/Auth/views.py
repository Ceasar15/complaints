from sqlite3 import IntegrityError

from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import logout

from .models import Profile, EmergencyContacts
from .serializers import RegisterSerializer, \
    MyTokenObtainPairSerializer, ProfileSerializer, \
    ProfileSerializerGet, EmergencyContactsSerializer
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
    authentication_classes = (JWTAuthentication,)

    # def post(self, request, *args, **kwargs):
    #     user = self.request.user
    #     data = self.request.data
    #     data._mutable = True
    #     print("dsfs")
    #     data['user'] = user.id
    #     serializer = ProfileSerializer(data=self.request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return self.queryset.filter()


class ProfileViewGet(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializerGet
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = Profile.objects
    lookup_field = 'user_id'


def logout_view(request):
    logout(request)
    return ''


class EmergencyContactsView(generics.ListCreateAPIView):
    queryset = EmergencyContacts.objects
    serializer_class = EmergencyContactsSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)





