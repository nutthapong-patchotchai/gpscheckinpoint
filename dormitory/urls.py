from django.urls import path
from dormitory.views import (
                              ChoiceCreateAPIView,ChoiceDetailAPIView,
                              DormCreateAPIView,DormDetailAPIView,
                              DormDetailCreateAPIView,DormDetailDetailAPIView,
                              DormImageCreateAPIView,DormImageDetailAPIView,
                              DormOwnerCreateAPIView,DormOwnerDetailAPIView,
                              DormStyleCreateAPIView,DormStyleDetailAPIView,getDormAll,
                              AboutCreateAPIView,AboutDetailAPIView,Test,TestAPIView,DormListHome,
                              DormStyleSearchAPIView,UserDormAPIView,UserDormDetailAPIView,getMyDormAPIView,getDorm,DormCreateAPIView,getDormChoice,
                              getlatlong
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
     path("userdorm/", UserDormAPIView.as_view(), name='userdorm-list'),
     path("userdorm/<int:pk>", UserDormDetailAPIView.as_view(), name='userdorm-detail'),
     path("test/", Test.as_view()),
     path("dorm/home/", DormListHome.as_view()),
     path("dormstyle/search/", DormStyleSearchAPIView.as_view(), name='dormstyle-search'),
     path("getMyDorm/<int:pk>", getMyDormAPIView.as_view(), name='getMyDormAPIView-search'),
     path("getDorm/<int:pk>", getDorm.as_view(), name='getDorm-search'),
     path("testDorm/", DormCreateAPIView.as_view(), name='getDorm-search'), 
     path("getDormChoice/", getDormChoice.as_view(), name='getDormChoice-search'),
     path("getDormAll/", getDormAll.as_view(), name='getDormAll-search'),
     path("getlatlong/", getlatlong.as_view()), #อันใหม่วันที่ 22/09/2020
]