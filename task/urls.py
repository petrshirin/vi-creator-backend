from django.urls import path
from .views import TaskViewSet


urlpatterns = [
    path('task/', TaskViewSet.as_view(), name='api_task_list'),

]
