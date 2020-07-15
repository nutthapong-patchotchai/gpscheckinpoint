from rest_framework import serializers
from proflie.models import proflie


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = proflie
        exclude = ("id",)