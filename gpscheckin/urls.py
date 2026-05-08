"""gpscheckin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.conf.urls.static import static
from checkin.forms import StyledAuthenticationForm
from checkin.serializer.RegisterSerializer import (
    LoginAPIView,
    LogoutAPIView,
    UserRegistrationView,
)
from checkin.views.frontend import history as checkin_history
from checkin.views.frontend import home as checkin_home
from checkin.views.frontend import coins as coins_view
from checkin.views.frontend import register as register_view
from checkin.views.frontend import resolve_location
from dormitory.views import home as index

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=StyledAuthenticationForm,
        ),
        name='login',
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout',
    ),
    path('register/', register_view, name='register'),
    path('accounts/register/', register_view, name='accounts_register'),
    path('api/register/', UserRegistrationView.as_view(), name="api_register_legacy"),
    path('api/auth/register/', UserRegistrationView.as_view(), name="api_register"),
    path('api/auth/register-full/', UserRegistrationView.as_view(), name="api_register_full"),
    path('api/auth/login/', LoginAPIView.as_view(), name="api_login"),
    path('api/auth/logout/', LogoutAPIView.as_view(), name="api_logout"),
    path('api/', include("checkin.urls")),
    path('api/dorm/', include("dormitory.urls")),
    path('coins/', coins_view, name='coins'),
    path('checkin/resolve-location/', resolve_location, name='resolve_location'),
    path('checkin/history/', checkin_history, name='checkin_history'),
    path('checkin/', checkin_home, name='checkin_home'),
    path('', index, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
