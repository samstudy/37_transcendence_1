from django.shortcuts import render
from .models import UserInformation


def user_profile(request, pk):
    user = UserInformation.objects.get(pk=pk)
    return render(request, 'user.html', {'user': user})
