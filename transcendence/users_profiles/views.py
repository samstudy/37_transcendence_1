from django.views.generic import DetailView
from django.contrib.auth.models import User


class UserPageView(DetailView):
    model = User
    template_name = "user.html"

    def get_context_data(self, **kwargs):
        context = super(UserPageView, self).get_context_data(**kwargs)
        context['user'] = User.objects.filter(username=self.get_object())
        return context
