import csv,io

from django.db.models import Count, Max
from django.http import HttpResponse
from rest_framework import generics
from django.contrib.auth.models import User
from checkin.models import gps, point, profile
from checkin.models.address import Geography, Province, Amphur, District
from checkin.serializer.serializers import GpsSerializer, PointSerializer, UserSerializer, ProfileSerializer, GeographySerializer, ProvinceSerializer, AmphurSerializer, DistrictSerializer, ProfileFullSerializer
from checkin.serializer.RegisterSerializer import UserRegistrationView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import datetime #important if using timezones



class UserCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileCreateAPIView(generics.ListCreateAPIView):
    queryset = profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetailAPIView(APIView):
    def get(self, request,pk, format=None):
        queryset = profile.objects.get(user__id=pk)
        serializer = ProfileSerializer(queryset) 
        return Response(serializer.data)

class ProfileFullDetailAPIView(APIView):
    def get(self, request,pk, format=None):
        queryset = profile.objects.get(user__id=pk)
        serializer = ProfileFullSerializer(queryset) 
        return Response(serializer.data)

class GPSCreateAPIView(generics.ListCreateAPIView):
    queryset = gps.objects.all()
    serializer_class = GpsSerializer


class GPSDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = gps.objects.all()
    serializer_class = GpsSerializer

class GPSHistoryAPIView(APIView): 
     def get(self, request,pk, format=None): 
        queryset = gps.objects.filter(user__id=pk).order_by('-updated_at')
        serializer = GpsSerializer(queryset,many=True) 
        return Response(serializer.data) 

class GPSExistAPIView(APIView): 
     def get(self, request,pk, format=None): 
        today = datetime.now().date()
        queryset = gps.objects.filter(user__id=pk,created_at__gte=today).exists()
        serializer = GpsSerializer(queryset,many=True) 
        return Response({"result":queryset}) 


class PointCreateAPIView(generics.ListCreateAPIView):
    queryset = point.objects.all()
    serializer_class = PointSerializer


class PointDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = point.objects.all()
    serializer_class = PointSerializer

class PointUserDetailAPIView(APIView): 
    def get(self, request,pk, format=None):
        queryset = point.objects.filter(user__id=pk).order_by('-updated_at')
        serializer = PointSerializer(queryset,many=True) 
        return Response(serializer.data)

class GeoCreateAPIView(generics.ListCreateAPIView):
    queryset = Geography.objects.all()
    serializer_class = GeographySerializer

class GeoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Geography.objects.all()
    serializer_class = GeographySerializer

class ProvinceCreateAPIView(generics.ListCreateAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class ProvinceDetailAPIView(APIView):
    def get(self, request,pk, format=None):
        queryset = Province.objects.filter(geo__id=pk)
        serializer = ProvinceSerializer(queryset,many=True) 
        return Response( serializer.data)

class AmphurCreateAPIView(generics.ListCreateAPIView):
    queryset = Amphur.objects.all()
    serializer_class = AmphurSerializer

class AmphurDetailAPIView(APIView): 
    def get(self, request,pk, format=None):
        queryset = Amphur.objects.filter(province__id=pk)
        serializer = AmphurSerializer(queryset,many=True) 
        return Response(serializer.data)

class DistrictCreateAPIView(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class DistrictDetailAPIView(APIView): 
    def get(self, request,pk, format=None):
        queryset = District.objects.filter(amphur__id=pk)
        serializer = DistrictSerializer(queryset,many=True) 
        return Response(serializer.data)

class DistrictAllDetailAPIView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class ProvinceFullDetailAPIView(APIView):
    def post(self, request, format=None):
        name = request.data.get('province')
        distName = request.data.get('dist')
        provinceset = Province.objects.filter(name=name).first() 
        queryset = District.objects.filter(province__id=provinceset.id,name=distName).first()
        serializer = DistrictSerializer(queryset) 
        return Response(serializer.data)


def createcsv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Checkinlog.csv"; encoding="utf-8-sig"'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(["รหัสนิสิต", "ภาค", "จังหวัด", "มีไข้", "ไอ", "มีน้ำมูก", "เจ็บคอ"
                     , "หายใจเร็วหรือหายใจลำบาก", "จมูกเริ่มไม่ได้กลิ่น", "ปรกติ",
                     "วันที่เช็คอิน", "เบอร์โทร", "ชื่อหอ"])

    for obj in gps.objects.all().order_by('-user__email', 'created_at').reverse():
        if gps.objects.filter(user__email=obj.user.email).count() > 1:
            if gps.objects.filter(user__email=obj.user.email).exists():
                writer.writerow([obj.user.email, obj.geo, obj.province, obj.sick1,
                             obj.sick2, obj.sick3, obj.sick4, obj.sick5, obj.sick6,
                             obj.sick7, obj.created_at, obj.user.profile.tel,
                             obj.user.profile.address2])
        else:
            writer.writerow([obj.user.email, obj.geo, obj.province, obj.sick1,
                             obj.sick2, obj.sick3, obj.sick4, obj.sick5, obj.sick6,
                             obj.sick7, obj.created_at, obj.user.profile.tel,
                             obj.user.profile.address2])



    return response