from rest_framework import serializers
from dormitory.models import (Choice, Dorm, DormDetail, DormStyle, DormImage, DormOwner ,About)
from django.db import models



class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('__all__')

class DormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dorm
        fields = ('__all__')

class DormDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DormDetail
        fields = ('__all__')

#อันนี้ไว้ค้นหา DormStyleนะ GETอย่างเดียว  ใช้ตัวนี้path("dormstyle/search/", DormStyleSearchAPIView.as_view(), name='dormstyle-search')
class DormStyleSearchSerializer(serializers.ModelSerializer):
    dorm = DormSerializer(read_only=True)
    choice = ChoiceSerializer(read_only=True)
    class Meta:
        model = DormStyle
        fields = ('dorm','choice')

#อันนี้ไว้ POST GET PATCH DELETE DormStyle
class DormStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DormStyle
        fields = ('__all__')



class DormImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DormImage
        fields = ('__all__')

class DormOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DormOwner
        fields = ('__all__')

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ('__all__')

