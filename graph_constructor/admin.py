from django.contrib import admin
from .models import GraphSettings, UserGraphConstructor, UserEmotion

admin.site.register(GraphSettings)
admin.site.register(UserGraphConstructor)
admin.site.register(UserEmotion)
