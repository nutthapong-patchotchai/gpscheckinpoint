from rest_framework import generics

from proflie.models import proflie
from proflie.api.serializers import ProfileSerializer


class ProfilesCreateAPIView(generics.ListCreateAPIView):
    queryset = proflie.objects.all()
    serializer_class = ProfileSerializer


class ProfilesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = proflie.objects.all()
    serializer_class = ProfileSerializer