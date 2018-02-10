from django.contrib import admin
from django.urls import path
from first_iteration import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/<pk>', views.user_profile, name='user_profile'),
]
