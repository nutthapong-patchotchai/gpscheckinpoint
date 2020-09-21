from rest_framework import serializers
from checkin.models import gps, point
from checkin.models.user import profile
from checkin.models.address import Geography, Province, Amphur, District
from checkin.models.checkin import cut_coin, user_cut_coin
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'is_staff']


class ProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    class Meta:
        model = profile
        fields = ('__all__')


class GpsSerializer(serializers.ModelSerializer):

    class Meta:
        model = gps
        exclude = ("id",)


class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = point
        fields = ('__all__')

class GeographySerializer(serializers.ModelSerializer): 
    class Meta:
        model = Geography
        fields = ('__all__')

class ProvinceSerializer(serializers.ModelSerializer): 
    geo = GeographySerializer(read_only=True) 
    class Meta:
        model = Province
        fields = ('__all__') 

class AmphurSerializer(serializers.ModelSerializer): 
    province = ProvinceSerializer(read_only=True)
    class Meta:
        model = Amphur
        fields = ('__all__')  

class DistrictSerializer(serializers.ModelSerializer): 
    amphur = AmphurSerializer(read_only=True)
    class Meta:
        model = District
        fields = ('__all__')

class ProfileFullSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    geo = GeographySerializer(read_only=True)
    province = ProvinceSerializer(read_only=True)
    amphur = AmphurSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    class Meta:
        model = profile
        fields = ('__all__')
#เพิ่มมาใหม่
class CutCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = cut_coin
        fields = ('__all__')
#เพิ่มมาใหม่
class UserCutCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_cut_coin
        fields = ('__all__')

class UserCutFullCoinSerializer(serializers.ModelSerializer):
    cut_coin = CutCoinSerializer(read_only=True)
    class Meta:
        model = user_cut_coin
        fields = ('__all__')