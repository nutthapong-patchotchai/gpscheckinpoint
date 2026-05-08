import csv

from django.http import HttpResponse
from rest_framework import generics, status
from django.contrib.auth.models import User
from checkin.models.user import profile
from checkin.models.address import Geography, Province, Amphur, District
from checkin.models.checkin import cut_coin, user_cut_coin, gps, point
from checkin.serializer.serializers import (GpsSerializer, PointSerializer, UserSerializer, 
                                            ProfileSerializer, GeographySerializer, ProvinceSerializer, 
                                            AmphurSerializer, DistrictSerializer, ProfileFullSerializer,UserCutFullCoinSerializer,
                                            CutCoinSerializer, UserCutCoinSerializer)
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
import datetime as docdate 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from checkin.services import (
    CoinError,
    InsufficientCoins,
    award_daily_checkin_coins,
    redeem_activity_reward,
)

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

    def perform_create(self, serializer):
        checkin = serializer.save()
        award_daily_checkin_coins(checkin)


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
    permission_classes = [IsAuthenticated]
    def get(self, request,pk, format=None): 
        today = datetime.now().date()
        queryset = gps.objects.filter(user__id=pk,created_at__gte=today).exists()
        return Response({"result":queryset}) 


class PointCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = point.objects.all()
    serializer_class = PointSerializer


class PointDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = point.objects.all()
    serializer_class = PointSerializer

class PointUserDetailAPIView(APIView): 
    permission_classes = [IsAuthenticated]
    def get(self, request,pk, format=None):
        queryset = point.objects.filter(user__id=pk).order_by('-updated_at')
        serializer = PointSerializer(queryset,many=True) 
        return Response(serializer.data)

class GeoCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Geography.objects.all()
    serializer_class = GeographySerializer

class GeoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Geography.objects.all()
    serializer_class = GeographySerializer

class ProvinceCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class ProvinceDetailAPIView(APIView):
    def get(self, request,pk, format=None):
        queryset = Province.objects.filter(geo__id=pk)
        serializer = ProvinceSerializer(queryset,many=True) 
        return Response( serializer.data)

class AmphurCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Amphur.objects.all()
    serializer_class = AmphurSerializer

class AmphurDetailAPIView(APIView): 
    def get(self, request,pk, format=None):
        queryset = Amphur.objects.filter(province__id=pk)
        serializer = AmphurSerializer(queryset,many=True) 
        return Response(serializer.data)

class DistrictCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class DistrictDetailAPIView(APIView): 
    def get(self, request,pk, format=None):
        queryset = District.objects.filter(amphur__id=pk)
        serializer = DistrictSerializer(queryset,many=True) 
        return Response(serializer.data)

class DistrictAllDetailAPIView(generics.RetrieveUpdateDestroyAPIView): 
    permission_classes = [IsAuthenticatedOrReadOnly]
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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = cut_coin.objects.all()
    serializer_class = CutCoinSerializer


class CutCoinDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = cut_coin.objects.all()
    serializer_class = CutCoinSerializer

class UserCutCoinAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = user_cut_coin.objects.all()
    serializer_class = UserCutCoinSerializer

    def create(self, request, *args, **kwargs):
        reward_id = request.data.get("cut_coin")
        if not reward_id:
            return Response({"detail": "กรุณาเลือกรายการแลก"}, status=status.HTTP_400_BAD_REQUEST)

        reward = cut_coin.objects.filter(pk=reward_id, status=True).first()
        if reward is None:
            return Response({"detail": "ไม่พบรายการแลกที่เปิดใช้งาน"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        requested_user_id = request.data.get("user")
        if requested_user_id and str(requested_user_id) != str(request.user.id):
            if not request.user.is_staff:
                return Response({"detail": "ไม่สามารถแลกให้ผู้ใช้อื่นได้"}, status=status.HTTP_403_FORBIDDEN)
            user = User.objects.filter(pk=requested_user_id).first()
            if user is None:
                return Response({"detail": "ไม่พบผู้ใช้"}, status=status.HTTP_404_NOT_FOUND)

        try:
            redemption = redeem_activity_reward(user, reward)
        except InsufficientCoins:
            return Response({"detail": "เหรียญไม่พอสำหรับแลกรายการนี้"}, status=status.HTTP_400_BAD_REQUEST)
        except CoinError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(redemption)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserCutCoinDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = user_cut_coin.objects.all()
    serializer_class = UserCutCoinSerializer


class getMyCoinAPIView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self, request,pk, format=None):
        queryset = user_cut_coin.objects.filter(user__id=pk).order_by('-created_at')
        serializer = UserCutFullCoinSerializer(queryset,many=True) 
        return Response(serializer.data)
