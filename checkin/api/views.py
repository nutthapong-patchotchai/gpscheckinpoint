from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import generics

from checkin.models import gps, point
from checkin.api.serializers import GpsSerializer, PointSerializer


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


# class GPSListCreateAPIView(APIView):
#
#     def get(self, request):
#         Gps = gps.objects.all()
#         serializer = GpsSerializer(Gps, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = GpsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class GPSDetailAPIView(APIView):
#
#     def get_object(self, pk):
#         Gps = get_object_or_404(gps, pk=pk)
#         return Gps
#
#     def get(self, request, pk):
#         Gps = self.get_object(pk)
#         serializer = GpsSerializer(Gps)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         Gps = self.get_object(pk)
#         serializer = GpsSerializer(Gps, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         Gps = self.get_object(pk)
#         Gps.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
