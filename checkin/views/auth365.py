from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import requests
from django.conf import settings
from requests_oauthlib import OAuth2Session



# Create your views here.
class Callback(APIView):
    @csrf_exempt
    def get(self, request, format=None):
         
         return Response( {})

    @csrf_exempt
    def post(self, request, format=None): 
        post_data = {
            'client_id':request.data.get('clientId'),
            "code":request.data.get('code'),
            'redirect_uri':request.data.get('redirectUri'),
            'grant_type':settings.UP_AUTH['GRANT_TYPE'],
            'client_secret': settings.UP_AUTH['SECRET_KEY']
        }
        response = requests.post(settings.AUTH_URL, data=post_data)
        response = json.loads(response.content)
         
        response = requests.get(settings.AUTH_PROFILE_URL,headers={"Authorization": f"Bearer "+response["access_token"]})
        response = json.loads(response.content)
        return Response(response)

    def put(self, request, id, format=None):
         return Response({}, status=400)

    def delete(self, request, id, format=None):
         return Response(status=204)

    
