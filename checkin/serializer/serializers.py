from rest_framework import serializers
from checkin.models import gps, point
from checkin.models.user import profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_staff']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
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
        exclude = ("id",)

