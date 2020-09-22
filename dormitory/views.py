from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from dormitory.models import (Choice, Dorm, DormDetail, DormStyle, DormImage, DormOwner, About, UserDorm)
from dormitory.serializer.serializers import (ChoiceSerializer, DormSerializer,
                                              DormStyleSerializer, DormImageSerializer,
                                              DormOwnerSerializer, AboutSerializer,
                                              DormDetailSerializer,DormStyleSearchSerializer,DormFullSerializer,
                                              UserDormSerializer,ZoneLatLong)
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import render
from django_filters import Filter, FilterSet
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from dormitory.filter import ChoiceFilter, DormStyleFilter, BookFilterSet, ZoneFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response

from rest_framework import filters

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size' 


class PostLimitOffsetPagnation(PageNumberPagination):
    default_limit = 5
    page_size_query_param = 'page_size'

    max_limit = 10

 
def home(request):
    return render(request, 'app/index.html')
    



class ChoiceCreateAPIView(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ChoiceFilter

class ChoiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class DormCreateAPIView(generics.ListCreateAPIView):
    queryset = Dorm.objects.all()
    serializer_class = DormSerializer

class DormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dorm.objects.all()
    serializer_class = DormFullSerializer
    

class DormDetailCreateAPIView(generics.ListCreateAPIView):
    queryset = DormDetail.objects.all()
    serializer_class = DormDetailSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('fan_price_month','fan_price_day','air_price_month','air_price_day',)

class DormDetailDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DormDetail.objects.all()
    serializer_class = DormDetailSerializer

class DormImageCreateAPIView(generics.ListCreateAPIView):
    queryset = DormImage.objects.all()
    serializer_class = DormImageSerializer

class DormImageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DormImage.objects.all()
    serializer_class = DormImageSerializer

class DormOwnerCreateAPIView(generics.ListCreateAPIView):
    queryset = DormOwner.objects.all()
    serializer_class = DormOwnerSerializer

class DormOwnerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DormOwner.objects.all()
    serializer_class = DormOwnerSerializer

class DormStyleCreateAPIView(generics.ListCreateAPIView):
    queryset = DormStyle.objects.all()
    serializer_class = DormStyleSerializer
    

class DormStyleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DormStyle.objects.all()
    serializer_class = DormStyleSerializer

class AboutCreateAPIView(generics.ListCreateAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

class AboutDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

class Test(APIView):
    def get(self, request, format=None):
        detail = DormDetail.objects.all()
        data = []
        for n in detail:
            price = 0
            if(n.fan_price_month > 0 and n.air_price_month > 0):
                price = n.fan_price_month
            else:
                price = n.air_price_month
            data.append({
                'dorm_id':n.dorm_id,
                'price' : price 
            })

        #     test = Dorm.objects.filter(name=n['name']).values_list('id', flat=True).first()
        #     choice = Choice.objects.filter(name="โซนหอพัก").filter(value=n['zone']).values_list('id', flat=True).first() 
        #     das.append(
        #         {
        #             "dorm_id":test,
        #             'zone':choice
        #         }
        #     )
        # choice = Choice.objects.filter(name="โซนหอพัก").filter(value="B").values_list('id', flat=True).first() 
        
        # queryset = DormStyle.objects.filter(choice=choice).values_list('dorm_id', flat=True) 
        return Response(data)

class TestAPIView(generics.ListCreateAPIView):
    queryset = Dorm.objects.all()
    serializer_class = DormSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name','geo',)

class DormListHome(generics.ListCreateAPIView):
    queryset = Dorm.objects.all().order_by('id')[:10:1]
    serializer_class = DormFullSerializer


class DormStyleSearchAPIView(generics.ListCreateAPIView):
    queryset = DormStyle.objects.all()
    serializer_class = DormStyleSearchSerializer
    pagination_class = PostLimitOffsetPagnation
    filter_backends = (DjangoFilterBackend,)
    #เอามาจากไฟล์ filter.py
    filter_class = DormStyleFilter
    pagination_class = PostLimitOffsetPagnation

#เพิ่มมาใหม่
class UserDormAPIView(generics.ListCreateAPIView):
    queryset = UserDorm.objects.all()
    serializer_class = UserDormSerializer
#เพิ่มมาใหม่
class UserDormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserDorm.objects.all()
    serializer_class = UserDormSerializer

class getMyDormAPIView(APIView): 
    def get(self, request,pk, format=None):
        queryset = UserDorm.objects.filter(user__id=pk).order_by('-created_at')
        serializer = UserDormSerializer(queryset,many=True) 
        return Response(serializer.data)

class getDorm(APIView): 
    def get(self, request,pk, format=None):
        queryset = Dorm.objects.all().order_by('id')
        serializer = DormFullSerializer(queryset,many=True) 
        return Response(serializer.data)

class DormCreateAPIView(generics.ListCreateAPIView):
    queryset = Dorm.objects.all()
    serializer_class = DormFullSerializer    
    filter_backends = (DjangoFilterBackend,filters.SearchFilter) 
    filter_class = BookFilterSet
    search_fields = ['name']
    pagination_class = LargeResultsSetPagination

class getDormChoice(APIView): 
    def get(self, request, format=None):
        id_choice = request.GET["id"]
        id_choice = id_choice.split(',')
        dorm = DormStyle.objects.filter(choice__in=id_choice).values_list('dorm', flat=True).all() 
        ids = {each: each for each in dorm}.values()
        return Response({"id" : ids})

class getDormAll(generics.ListCreateAPIView): 
    queryset = Dorm.objects.all()
    serializer_class = DormSerializer 
        
#อันใหม่วันที่ 22/09/2020        
class getlatlong(generics.ListAPIView):
    queryset = Dorm.objects.all()
    serializer_class = ZoneLatLong
    filter_backends = (DjangoFilterBackend,)
    filter_class = ZoneFilter
