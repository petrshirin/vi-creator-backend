from .models import UserGraphConstructor
from rest_framework import serializers
from django.utils.translation import gettext_lazy as l_


class UserGraphConstructorSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGraphConstructor
        fields = [
            'content',
            'is_active',
            'mark',
        ]


class SetActiveGraphSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGraphConstructor
        fields = [
            'id'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(SetActiveGraphSerializer, self).__init__(args, kwargs)

    def validate(self, data):
        validated_data = super(SetActiveGraphSerializer, self).validate(data)
        if self.request.user != self.instance.user or \
                self.request.user.get_my_teacher() != self.instance.user.get_my_teacher():
            raise serializers.ValidationError({'Id': l_('У нас не доступа к этому графу')})
        return validated_data
