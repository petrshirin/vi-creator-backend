from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('graph/', include('graph_constructor.urls')),
    # path('task/', include('task.urls')),
    # path('core/', include('core.urls')),
    # path('execute/', include('code_executor.urls')),
]











