import csv,io

from django.db.models import Count, Max
from django.http import HttpResponse
from rest_framework import generics
from django.contrib.auth.models import User
from checkin.models.user import profile
from checkin.models.address import Geography, Province, Amphur, District
from checkin.models.checkin import cut_coin, user_cut_coin, gps, point
from checkin.serializer.serializers import (GpsSerializer, PointSerializer, UserSerializer, 
                                            ProfileSerializer, GeographySerializer, ProvinceSerializer, 
                                            AmphurSerializer, DistrictSerializer, ProfileFullSerializer,
                                            CutCoinSerializer, UserCutCoinSerializer)
from checkin.serializer.RegisterSerializer import UserRegistrationView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import datetime #important if using timezones
from datetime import datetime, time
import datetime as docdate 
from rest_framework.permissions import IsAuthenticated

class UserCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,pk, format=None):
        queryset = profile.objects.get(user__id=pk)
        serializer = ProfileSerializer(queryset) 
        return Response(serializer.data)

class ProfileFullDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,pk, format=None):
        queryset = profile.objects.get(user__id=pk)
        serializer = ProfileFullSerializer(queryset) 
        return Response(serializer.data)
    def put(self, request, pk=None):
        try:
            item = profile.objects.get(pk=pk)
        except profile.DoesNotExist:
            return Response(status=404)
        serializer = ProfileFullSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class GPSCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = gps.objects.all()
    serializer_class = GpsSerializer


class GPSDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = gps.objects.all()
    serializer_class = GpsSerializer

class GPSHistoryAPIView(APIView): 
    permission_classes = [IsAuthenticated]
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
def splitStr(str):
    output = str.split('@')
    return output[0]
def dateConvert(strr):
    ds = str(strr).split(" ")
    ds = ds[0]
    dd = docdate.datetime.strptime(ds, "%Y-%m-%d").strftime('%d/%m/%Y')
    return dd
def phoneFormat(num):
    dd = str(num)
    if ((len(dd)) == 10):
        dd = format(int(dd[:-1]), ",").replace(",", "-") + dd[-1]
        dd = "0"+dd
    return dd
class createcsv(APIView):
    def get(self, request,format=None):

      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="Checkinlog.csv"; encoding="utf-8-sig"'
      response.write(u'\ufeff'.encode('utf8'))

      writer = csv.writer(response)
      writer.writerow(["รหัสนิสิต", "ภาค", "จังหวัด", "มีไข้", "ไอ", "มีน้ำมูก", "เจ็บคอ"
                       , "หายใจเร็วหรือหายใจลำบาก", "จมูกเริ่มไม่ได้กลิ่น", "ปกติ",
                       "วันที่เช็คอิน", "เบอร์โทร", "ชื่อหอ","latitude","longitude"])

      tmp = gps.objects.all().order_by('user__email','created_at').values('id', 'user_id')
      unique = {each['user_id']: each['id'] for each in tmp}.values()
      queryset = gps.objects.filter(id__in=unique)\
        .values('user_id','user__email','geo__name','province__name',
                'sick1','sick2','sick3','sick4','sick5','sick6','sick7',
                'created_at','user__profile__tel','user__profile__address2',
                'latitude','longitude')
      output = []
      for data in queryset:
        writer.writerow([
            splitStr(data['user__email']),
            data['geo__name'],
            data['province__name'],
            data['sick1'],
            data['sick2'],
            data['sick3'],
            data['sick4'],
            data['sick5'],
            data['sick6'],
            data['sick7'],
            dateConvert(data['created_at']),
            phoneFormat(str(data['user__profile__tel'])),
            data['user__profile__address2'],
            data['latitude'],
            data['longitude']
        ])
      return response

#เพิ่ม cutcoin เข้ามาใหม่
class CutCoinAPIView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = cut_coin.objects.all()
    serializer_class = CutCoinSerializer


class CutCoinDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = cut_coin.objects.all()
    serializer_class = CutCoinSerializer

class UserCutCoinAPIView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = user_cut_coin.objects.all()
    serializer_class = UserCutCoinSerializer


class UserCutCoinDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = user_cut_coin.objects.all()
    serializer_class = UserCutCoinSerializer
