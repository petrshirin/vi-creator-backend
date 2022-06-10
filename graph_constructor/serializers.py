

from .models import UserGraphConstructor
from rest_framework import serializers


class UserGraphConstructorSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGraphConstructor
        fields = [
            'content',
            'is_active',
            'mark',
        ]
