import csv,io
from django.http import HttpResponse
from rest_framework import generics
from django.contrib.auth.models import User
from checkin.models import gps, point, profile
from checkin.serializer.serializers import GpsSerializer, PointSerializer, UserSerializer


class UserCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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


def createcsv(request):
    items = gps.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Checkinlog.csv"; encoding="utf-8-sig"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(["รหัสนิสิต", "ภาค", "จังหวัด","มีไข้"])

    for obj in items:
        writer.writerow([obj.user.email, obj.geo, obj.province, obj.sick1])


    return response