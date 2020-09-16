from django.urls import path
from dormitory.views import (
                              ChoiceCreateAPIView,ChoiceDetailAPIView,
                              DormCreateAPIView,DormDetailAPIView,
                              DormDetailCreateAPIView,DormDetailDetailAPIView,
                              DormImageCreateAPIView,DormImageDetailAPIView,
                              DormOwnerCreateAPIView,DormOwnerDetailAPIView,
                              DormStyleCreateAPIView,DormStyleDetailAPIView,
                              AboutCreateAPIView,AboutDetailAPIView
                              )

urlpatterns = [
     path("choice/", ChoiceCreateAPIView.as_view(), name='choice-list'),
     path("choice/<int:pk>", ChoiceDetailAPIView.as_view(), name='choice-detail'),
     path("dorm/", DormCreateAPIView.as_view(), name='dorm-list'),
     path("dorm/<int:pk>", DormDetailAPIView.as_view(), name='dorm-detail'),
     path("dormdetail/", DormDetailCreateAPIView.as_view(), name='dormdetail-list'),
     path("dormdetail/<int:pk>", DormDetailDetailAPIView.as_view(), name='dormdetail-detail'),
     path("dormimage/", DormImageCreateAPIView.as_view(), name='dormimage-list'),
     path("dormimage/<int:pk>", DormImageDetailAPIView.as_view(), name='dormimage-detail'),
     path("dormowner/", DormOwnerCreateAPIView.as_view(), name='dormowner-list'),
     path("dormowner/<int:pk>", DormOwnerDetailAPIView.as_view(), name='dormowner-detail'),
     path("dormstyle/", DormStyleCreateAPIView.as_view(), name='dormstyle-list'),
     path("dormstyle/<int:pk>", DormStyleDetailAPIView.as_view(), name='dormstyle-detail'),
     path("about/", AboutCreateAPIView.as_view(), name='about-list'),
     path("about/<int:pk>", AboutDetailAPIView.as_view(), name='about-detail'),
]