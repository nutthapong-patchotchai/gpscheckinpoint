from django.urls import path
from checkin.views.views import (GPSCreateAPIView,
                                 GPSDetailAPIView,
                                 PointCreateAPIView,
                                 PointDetailAPIView)


urlpatterns = [
    path("", GPSCreateAPIView.as_view(), name='gps-list'),
    path("gps/<int:pk>", GPSDetailAPIView.as_view(), name='gps-detail'),
    path("ponit/", PointCreateAPIView.as_view(), name='point-list'),
    path("ponit/<int:pk>", PointDetailAPIView.as_view(), name='point-detail')
]