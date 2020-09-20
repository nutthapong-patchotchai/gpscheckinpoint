from django.urls import path
from checkin.views.views import (GPSCreateAPIView, GPSDetailAPIView,
                                 PointCreateAPIView, PointDetailAPIView,
                                 UserCreateAPIView, UserDetailAPIView,
                                 ProfileCreateAPIView, ProfileDetailAPIView,
                                 GeoCreateAPIView, GeoDetailAPIView,
                                 ProvinceCreateAPIView, ProvinceDetailAPIView, 
                                 AmphurCreateAPIView, AmphurDetailAPIView,
                                 DistrictCreateAPIView, DistrictDetailAPIView, ProfileFullDetailAPIView,
                                 DistrictAllDetailAPIView,ProvinceFullDetailAPIView, PointUserDetailAPIView, 
                                 GPSHistoryAPIView, GPSExistAPIView,
                                 createcsv, CutCoinAPIView, CutCoinDetailAPIView,
                                 UserCutCoinAPIView, UserCutCoinDetailAPIView
                                 )


urlpatterns = [
    path("gps/", GPSCreateAPIView.as_view(), name='gps-list'),
    path("gps/<int:pk>", GPSDetailAPIView.as_view(), name='gps-detail'),
    path("ponit/", PointCreateAPIView.as_view(), name='point-list'),
    path("ponit/<int:pk>", PointDetailAPIView.as_view(), name='point-detail'), 
    path("ponituser/<int:pk>", PointUserDetailAPIView.as_view(), name='point-user-detail'),
    path("register/", UserCreateAPIView.as_view(), name='register'),
    path("user/<int:pk>/edit", UserDetailAPIView.as_view(), name='user-detail'),
    path("profile/", ProfileCreateAPIView.as_view(), name='profile'),
    path("profile/<int:pk>/", ProfileDetailAPIView.as_view(), name='profile-detail'),
    path("geo/", GeoCreateAPIView.as_view(), name='profile'),
    path("geo/<int:pk>/", GeoDetailAPIView.as_view(), name='profile-detail'),
    path("province/", ProvinceCreateAPIView.as_view(), name='province'),
    path("province/<int:pk>/", ProvinceDetailAPIView.as_view(), name='province-detail'),
    path("amphur/", AmphurCreateAPIView.as_view(), name='amphur'),
    path("amphur/<int:pk>/", AmphurDetailAPIView.as_view(), name='amphur-detail'),
    path("district/", DistrictCreateAPIView.as_view(), name='district'),
    path("district/<int:pk>/", DistrictDetailAPIView.as_view(), name='district-detail'),
    path("profilefull/<int:pk>/", ProfileFullDetailAPIView.as_view(), name='profilefull-detail'),
    path("districtfull/<int:pk>/", DistrictAllDetailAPIView.as_view(), name='districtfull-detail'),
    path("provincesearch/", ProvinceFullDetailAPIView.as_view(), name='provinprovincesearchce'),
    path("gps/history/<int:pk>/", GPSHistoryAPIView.as_view(), name='GPSHistoryAPIView'),
    path("gps/exist/<int:pk>/", GPSExistAPIView.as_view(), name='GPSExistAPIView'),
    path("cut-coin/", CutCoinAPIView.as_view(), name='cut-coin'), #เพิ่มมาใหม่
    path("cut-coin/<int:pk>/", CutCoinDetailAPIView.as_view(), name='cut-coin-detail'), #เพิ่มมาใหม่
    path("user-cut-coin/", UserCutCoinAPIView.as_view(), name='user-cut-coin'), #เพิ่มมาใหม่
    path("user-cut-coin/<int:pk>/", UserCutCoinDetailAPIView.as_view(), name='user-cut-coin-detail'), #เพิ่มมาใหม่
    path("doc/create", createcsv.as_view(), name='Document'),
]