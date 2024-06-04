"""
URL configuration for neighborhost project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import index
from app.views import home
from app.views import view_event_from_signout
from app.views import signup
from app.views import account_verify_from_signup
from app.views import skip_verification
from app.views import login
from app.views import account_verify_from_login
from app.views import verify_with_code
from app.views import verified
from app.views import friends_check
from app.views import plan_event
from app.views import filter_location
from app.views import filter_view
from app.views import filter_calendar
from app.views import filter_date
from app.views import view_event_from_login
from app.views import friend_profile
from app.views import friend_request
from app.views import signout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('view_event_from_signout/', view_event_from_signout, name='view_event_from_signout'),
    path('signup/', signup, name='signup'),
    path('account_verify_from_signup/', account_verify_from_signup, name='account_verify_from_signup'),
    path('skip_verification/', skip_verification, name='skip_verification'),
    path('login/', login, name='login'),
    path('account_verify_from_login/', account_verify_from_login, name='account_verify_from_login'),
    path('verify_with_code/', verify_with_code, name='verify_with_code'),
    path('verified/', verified, name='verified'),
    path('friends_check/', friends_check, name='friends_check'),
    path('plan_event/', plan_event, name='plan_event'),
    path('filter_location/', filter_location, name='filter_location'),
    path('filter_view/', filter_view, name='filter_view'),
    path('filter_calendar/', filter_calendar, name='filter_calendar'),
    path('filter_date/', filter_date, name='filter_date'),
    path('view_event_from_login/', view_event_from_login, name='view_event_from_login'),
    path('friend_profile/', friend_profile, name='friend_profile'),
    path('friend_request/', friend_request, name='friend_request'),
    path('signout/', signout, name='signout')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)