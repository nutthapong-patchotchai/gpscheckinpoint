from django.urls import path
from proflie.api.views import (ProfilesCreateAPIView,
                               ProfilesDetailAPIView,
                               )


urlpatterns = [
    path("profile/", ProfilesCreateAPIView.as_view(), name='profile-list'),
    path("profile/<int:pk>", ProfilesDetailAPIView.as_view(), name='profile-detail'),
]