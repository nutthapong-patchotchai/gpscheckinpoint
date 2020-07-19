from django.views.decorators.csrf import csrf_exempt
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView
from rest_framework import serializers
from checkin.models.checkin import gps, point
from checkin.models.user import profile
from checkin.models.address import *
from django.contrib.auth.models import User


class RegistrationSerializer(RegisterSerializer):

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False) 
    address = serializers.CharField(required=False)
    geo = serializers.CharField(required=False)
    amphur = serializers.CharField(required=False)
    province = serializers.CharField(required=False)
    district = serializers.CharField(required=False)
    post = serializers.CharField(required=False)
    tel = serializers.CharField(required=False)
    question1 = serializers.CharField(required=False)
    question2 = serializers.CharField(required=False)
    question3 = serializers.CharField(required=False)
    address2 = serializers.CharField(required=False)


@csrf_exempt
def custom_signup(self, request, user):
    user.first_name = self.validated_data.get('first_name', '')
    user.last_name = self.validated_data.get('last_name', '')
    user.save(update_fields=['first_name', 'last_name'])
    user_profile = profile()
    user_profile.user = user 
    user_profile.address = self.validated_data.get('address', '')
    user_profile.geo = self.validated_data.get('geo', 0.00)
    user_profile.amphur = self.validated_data.get('amphur', 0.00)
    user_profile.province = self.validated_data.get('province', '')
    user_profile.district = self.validated_data.get('district', '')
    user_profile.post = self.validated_data.get('post', 0.00)
    user_profile.tel = self.validated_data.get('tel', 0.00) 
    user_profile.question1 = self.validated_data.get('question1', '')
    user_profile.question2 = self.validated_data.get('question2', 0.00)
    user_profile.question3 = self.validated_data.get('question3', 0.00)
    user_profile.address2 = self.validated_data.get('address2', 0.00)
    user_profile.save()


class UserRegistrationView(RegisterView):
    serializer_class = RegistrationSerializer
