from django.urls import path
from .views import RegisterView, MyStudentView, MyUserView
from rest_framework.authtoken.views import ObtainAuthToken as LoginView


urlpatterns = [
    path('login/', LoginView.as_view(), name='api_login'),
    path('register/', RegisterView.as_view(), name='api_register'),
    path('students/', MyStudentView.as_view(), name='students_list'),
    path('user/my/', MyUserView.as_view(), name='my_info'),
]
