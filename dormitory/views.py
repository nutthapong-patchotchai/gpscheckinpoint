from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from dormitory.models import (Choice, Dorm, DormDetail, DormStyle, DormImage, DormOwner, About, UserDorm)
from dormitory.serializer.serializers import (ChoiceSerializer, DormSerializer,
                                              DormStyleSerializer, DormImageSerializer,
                                              DormOwnerSerializer, AboutSerializer,
                                              DormDetailSerializer,DormStyleSearchSerializer,DormFullSerializer,
                                              UserDormSerializer,ZoneLatLong)
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from dormitory.filter import ChoiceFilter, DormStyleFilter, BookFilterSet, ZoneFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from checkin.models.checkin import gps

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size' 


class PostLimitOffsetPagnation(PageNumberPagination):
    default_limit = 5
    page_size_query_param = 'page_size'

    max_limit = 10

 
def home(request):
    query = request.GET.get("q", "").strip()
    dorms = (
        Dorm.objects.filter(advt=True)
        .select_related("geo", "province", "amphur", "district")
        .order_by("name")
    )
    if query:
        dorms = dorms.filter(
            Q(name__icontains=query)
            | Q(address__icontains=query)
            | Q(tel__icontains=query)
            | Q(province__name__icontains=query)
            | Q(amphur__name__icontains=query)
            | Q(district__name__icontains=query)
        )

    context = {
        "query": query,
        "dorms": dorms[:24],
        "dorm_count": Dorm.objects.count(),
        "public_dorm_count": Dorm.objects.filter(advt=True).count(),
        "checkin_count": gps.objects.count(),
        "latest_checkin": None,
    }
    if request.user.is_authenticated:
        context["latest_checkin"] = (
            gps.objects.filter(user=request.user)
            .select_related("province", "amphur", "district")
            .order_by("-created_at")
            .first()
        )
    return render(request, "dormitory/home.html", context)
    



class ChoiceCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ChoiceFilter

class ChoiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class DormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Dorm.objects.all()
    serializer_class = DormFullSerializer
    

class DormDetailCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DormDetail.objects.all()
    serializer_class = DormDetailSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('fan_price_month','fan_price_day','air_price_month','air_price_day',)

class DormDetailDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DormDetail.objects.all()
    serializer_class = DormDetailSerializer

class DormImageCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DormImage.objects.all()
    serializer_class = DormImageSerializer

class DormImageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DormImage.objects.all()
    serializer_class = DormImageSerializer

class DormOwnerCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DormOwner.objects.all()
    serializer_class = DormOwnerSerializer

class DormOwnerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DormOwner.objects.all()
    serializer_class = DormOwnerSerializer

class DormStyleCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DormStyle.objects.all()
    serializer_class = DormStyleSerializer
    

class DormStyleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DormStyle.objects.all()
    serializer_class = DormStyleSerializer

class AboutCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = About.objects.all()
    serializer_class = AboutSerializer

class AboutDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = About.objects.all()
    serializer_class = AboutSerializer

class Test(APIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Dorm.objects.all()
    serializer_class = DormSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name','geo',)

class DormListHome(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Dorm.objects.all().order_by('id')[:10]
    serializer_class = DormFullSerializer


class DormStyleSearchAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DormStyle.objects.all()
    serializer_class = DormStyleSearchSerializer
    pagination_class = PostLimitOffsetPagnation
    filter_backends = (DjangoFilterBackend,)
    #เอามาจากไฟล์ filter.py
    filterset_class = DormStyleFilter

#เพิ่มมาใหม่
class UserDormAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserDorm.objects.all()
    serializer_class = UserDormSerializer
#เพิ่มมาใหม่
class UserDormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserDorm.objects.all()
    serializer_class = UserDormSerializer

class getMyDormAPIView(APIView): 
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Dorm.objects.all()
    serializer_class = DormFullSerializer    
    filter_backends = (DjangoFilterBackend,filters.SearchFilter) 
    filterset_class = BookFilterSet
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Dorm.objects.all()
    serializer_class = DormSerializer 
        
#อันใหม่วันที่ 22/09/2020        
class getlatlong(generics.ListAPIView):
    queryset = Dorm.objects.all()
    serializer_class = ZoneLatLong
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ZoneFilter
