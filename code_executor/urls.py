from django.urls import path
from .views import ExecuteCodeView, ConsoleCallbackView

urlpatterns = [
    path('run/', ExecuteCodeView.as_view(), name='run_code'),
    path('logs/', ConsoleCallbackView.as_view(), name='update_user_console_content')
]
