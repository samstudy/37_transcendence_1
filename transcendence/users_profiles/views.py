from django.views.generic import DetailView
from django.contrib.auth.models import User


class UserPageView(DetailView):
    template_name = "users_profiles/user.html"
    model = User
    pk_url_kwarg = 'pk'
