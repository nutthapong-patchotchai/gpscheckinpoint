from django.shortcuts import render
from rest_framework import generics
from dormitory.models import Zonedorm, Typedorm, Sizedorm, Pricedorm, Pet, Makefood, Dormitory
from dormitory.serializer.serializers import (TypedormSerializer,ZonedormSerializer,SizedormSerializer,PricedormSerializer,PetSerializer,MakefoodSerializer,DormitorySerializer)

class ZonedormCreateAPIView(generics.ListCreateAPIView):
    queryset = Zonedorm.objects.all()
    serializer_class = ZonedormSerializer

class ZonedormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zonedorm.objects.all()
    serializer_class = ZonedormSerializer

class TypedormCreateAPIView(generics.ListCreateAPIView):
    queryset = Typedorm.objects.all()
    serializer_class = TypedormSerializer

class TypedormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Typedorm.objects.all()
    serializer_class = TypedormSerializer

class SizedormCreateAPIView(generics.ListCreateAPIView):
    queryset = Sizedorm.objects.all()
    serializer_class = SizedormSerializer

class SizedormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sizedorm.objects.all()
    serializer_class = SizedormSerializer

class PricedormCreateAPIView(generics.ListCreateAPIView):
    queryset = Pricedorm.objects.all()
    serializer_class = PricedormSerializer

class PricedormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pricedorm.objects.all()
    serializer_class = PricedormSerializer

class PetCreateAPIView(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class PetDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class MakefoodCreateAPIView(generics.ListCreateAPIView):
    queryset = Makefood.objects.all()
    serializer_class = MakefoodSerializer

class MakefoodDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Makefood.objects.all()
    serializer_class = MakefoodSerializer

class DormitoryCreateAPIView(generics.ListCreateAPIView):
    queryset = Dormitory.objects.all()
    serializer_class = DormitorySerializer

class DormitoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dormitory.objects.all()
    serializer_class = DormitorySerializer