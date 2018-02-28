from django.urls import path, include
from user_profiles.views import UserPageView


urlpatterns = [
    path('users/<pk>', UserPageView.as_view(), name='user')
]
