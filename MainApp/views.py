from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from django.views.generic import View
from django.views.generic.edit import CreateView

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


def ajax_validate(request):
    """
        Check user form fields
    """
    username = request.GET.get('username', None)
    already_exists = User.objects.filter(username__iexact=username).exists()
    response = {
        'already_exists': already_exists
    }
    return JsonResponse(response)


@login_required(login_url='/signup/')
def MainPage(request):
    return render(request, 'home.html')


class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        valid = super().form_valid(form)
        print(self.request)
        print(self.object)
        login(self.request, self.object)
        return valid

