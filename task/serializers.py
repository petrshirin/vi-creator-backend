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


class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAnswer
        fields = [
            'id',
            'task',
            'answer',
            'answer_graph',
            'mark',
            'status',
        ]


class UserAnswerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = [
            'task',
            'answer',
            'answer_graph',
        ]
        extra_kwargs = {
            'task': {'required': True},
            'answer': {'required': False},
            'answer_graph': {'required': False},
        }


class TeacherUserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = [
            'id',
            'task',
            'answer',
            'answer_graph',
            'mark',
            'status',
        ]
