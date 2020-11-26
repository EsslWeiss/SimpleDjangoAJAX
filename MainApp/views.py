from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import ContactForm


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

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        form.save()
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return redirect('/home/')


class ContactPage(FormView):
    template_name = 'contactpage.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        form.save()
        #return JsonResponse({'name': name}, status=200)
        return super().form_valid(form)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)

