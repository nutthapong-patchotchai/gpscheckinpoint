from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from dormitory.models import (Choice, Dorm, DormDetail, DormStyle, DormImage, DormOwner ,About)
from dormitory.serializer.serializers import (ChoiceSerializer, DormSerializer,
                                              DormStyleSerializer, DormImageSerializer,
                                              DormOwnerSerializer, AboutSerializer,
                                              DormDetailSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import render

 
def home(request):
    return render(request, 'app/index.html')

class ChoiceCreateAPIView(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name',)

    # def get_queryset(self):
    #     queryset = Choice.objects.all()
    #     active = self.request.query_params.get('name','')
    #     if active:
    #         if active == "False":
    #             active = False
    #         elif active == "True":
    #             active = True
    #         else:
    #             return queryset
    #         return queryset.filter(is_active=active)
    #     return queryset

class ChoiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class DormCreateAPIView(generics.ListCreateAPIView):
    queryset = Dorm.objects.all()
    serializer_class = DormSerializer

class DormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dorm.objects.all()
    serializer_class = DormSerializer

class DormDetailCreateAPIView(generics.ListCreateAPIView):
    queryset = DormDetail.objects.all()
    serializer_class = DormDetailSerializer

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
    serializer_class = DormSerializer