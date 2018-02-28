from django.urls import path, include
from users_profiles.views import UserPageView


urlpatterns = [
    path('users/<pk>', UserPageView.as_view(), name='user')
]
