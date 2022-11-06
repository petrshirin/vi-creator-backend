from django.urls import path
from .views import RegisterView
from rest_framework.authtoken.views import ObtainAuthToken as LoginView


urlpatterns = [
    path('login/', LoginView.as_view(), name='api_login'),
    path('register/', RegisterView.as_view(), name='api_register'),
]
