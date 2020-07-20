from django.urls import path
from checkin.views.views import (GPSCreateAPIView, GPSDetailAPIView,
                                 PointCreateAPIView, PointDetailAPIView,
                                 UserCreateAPIView, UserDetailAPIView,
                                 ProfileCreateAPIView, ProfileDetailAPIView)


urlpatterns = [
    path("gps/", GPSCreateAPIView.as_view(), name='gps-list'),
    path("gps/<int:pk>", GPSDetailAPIView.as_view(), name='gps-detail'),
    path("ponit/", PointCreateAPIView.as_view(), name='point-list'),
    path("ponit/<int:pk>", PointDetailAPIView.as_view(), name='point-detail'),
    path("register/", UserCreateAPIView.as_view(), name='register'),
    path("user/<int:pk>/edit", UserDetailAPIView.as_view(), name='user-detail'),
    path("profile/", ProfileCreateAPIView.as_view(), name='profile'),
    path("profile/<int:pk>/", ProfileDetailAPIView.as_view(), name='profile-detail'),

]