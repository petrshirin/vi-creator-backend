from rest_framework import serializers
from .models import UserExecuteSettings


class ExecuteCodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)


class ConsoleLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserExecuteSettings
        fields = ('user_id', 'console_content')
