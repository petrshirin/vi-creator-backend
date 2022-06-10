from .models import Task, UserAnswer
from rest_framework import serializers


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    """Класс для представления данных о задании ученику"""
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'description',
            'type',
            'auto_check',
        ]


class TaskTeacherSerializer(serializers.ModelSerializer):
    """Класс для представления данных о задании преподавателю"""
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'description',
            'type',
            'answer',
            'graph_answer',
            'max_mark',
        ]

