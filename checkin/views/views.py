from rest_framework import generics
from django.contrib.auth.models import User
from checkin.models import gps, point, profile
from checkin.serializer.serializers import GpsSerializer, PointSerializer, UserSerializer, ProfileSerializer
from checkin.serializer.RegisterSerializer import UserRegistrationView


class UserCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileCreateAPIView(generics.ListCreateAPIView):
    queryset = profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = profile.objects.all()
    serializer_class = ProfileSerializer


class GPSCreateAPIView(generics.ListCreateAPIView):
    queryset = gps.objects.all()
    serializer_class = GpsSerializer


class GPSDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = gps.objects.all()
    serializer_class = GpsSerializer


class PointCreateAPIView(generics.ListCreateAPIView):
    queryset = point.objects.all()
    serializer_class = PointSerializer


class PointDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = point.objects.all()
    serializer_class = PointSerializer