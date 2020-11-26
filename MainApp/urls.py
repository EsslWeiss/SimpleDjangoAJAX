from django.urls import path
from .views import MainPage, SignUpView, ajax_validate

urlpatterns = [
    path('home/', MainPage, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('validate/', ajax_validate, name='validate'),
]
