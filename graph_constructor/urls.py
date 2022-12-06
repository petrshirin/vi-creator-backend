from django.urls import path
from .views import GraphConstructorViewSet, ActiveGraphView


urlpatterns = [
    path('graph/', GraphConstructorViewSet.as_view(), name='api_graph_list'),
    path('graph/active/', ActiveGraphView.as_view(), name='api_active_graph'),
]
