from rest_framework import serializers
from dormitory.models import Dormitory, Zonedorm, Typedorm, Sizedorm, Pricedorm, Pet, Makefood

class ZonedormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zonedorm
        fields = ('__all__')

class TypedormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Typedorm
        fields = ('__all__')

class SizedormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sizedorm
        fields = ('__all__')

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('__all__')

class PricedormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricedorm
        fields = ('__all__')

class MakefoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Makefood
        fields = ('__all__')

class DormitorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Dormitory
        fields = ('__all__')