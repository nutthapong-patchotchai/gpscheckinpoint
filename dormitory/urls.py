from django.urls import path
from dormitory.views import (ZonedormCreateAPIView,ZonedormDetailAPIView,
                              TypedormCreateAPIView,TypedormDetailAPIView,
                              DormitoryCreateAPIView,DormitoryDetailAPIView,
                              SizedormCreateAPIView,SizedormDetailAPIView,
                              PricedormCreateAPIView,PricedormDetailAPIView,
                              PetCreateAPIView,PetDetailAPIView,
                              MakefoodCreateAPIView,MakefoodDetailAPIView,
                              )

urlpatterns = [
     path("zone/", ZonedormCreateAPIView.as_view(), name='zone-list'),
     path("zone/<int:pk>", ZonedormDetailAPIView.as_view(), name='zone-detail'),
     path("type/", TypedormCreateAPIView.as_view(), name='type-list'),
     path("type/<int:pk>", TypedormDetailAPIView.as_view(), name='type-detail'),
     path("size/", SizedormCreateAPIView.as_view(), name='size-list'),
     path("size/<int:pk>", SizedormDetailAPIView.as_view(), name='size-detail'),
     path("price/", PricedormCreateAPIView.as_view(), name='price-list'),
     path("price/<int:pk>", PricedormDetailAPIView.as_view(), name='price-detail'),
     path("pet/", PetCreateAPIView.as_view(), name='pet-list'),
     path("pet/<int:pk>", PetDetailAPIView.as_view(), name='pet-detail'),
     path("makefood/", MakefoodCreateAPIView.as_view(), name='makefood-list'),
     path("makefood/<int:pk>", MakefoodDetailAPIView.as_view(), name='makefood-detail'),
     path("dormitory/", DormitoryCreateAPIView.as_view(), name='dormitory-list'),
     path("dormitory/<int:pk>", DormitoryDetailAPIView.as_view(), name='dormitory-detail'),
]