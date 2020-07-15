from rest_framework import serializers
from checkin.models import gps, point


class GpsSerializer(serializers.ModelSerializer):

    class Meta:
        model = gps
        exclude = ("id",)



class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = point
        exclude = ("id",)

