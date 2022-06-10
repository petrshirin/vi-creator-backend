from django.db import models
from django.utils.translation import gettext as _, gettext_lazy as l_
from solo.models import SingletonModel

from core.models import User
from core.utils.upload import FileUploadTo


def get_emotion_upload(instance, filename):
    file_upload = FileUploadTo('user_emotion', 'user')
    return file_upload.get_file_path(instance, filename)


class GraphSettings(SingletonModel):
    max_nodes = models.PositiveIntegerField(verbose_name=_('Максимальное количество узлов'), default=30)
    max_edges = models.PositiveIntegerField(verbose_name=_('Максимальное количество ребер'), default=50)
    can_circle = models.BooleanField(verbose_name=_('Возможно зацикливание графа'))

    class Meta:
        verbose_name = l_('Настройки графа')


class UserGraphConstructor(models.Model):
    user = models.ForeignKey(User, related_name='graphs',
                             verbose_name=_('Пользователь'), on_delete=models.CASCADE)
    content = models.JSONField(verbose_name=_('Контент графа'), null=True, blank=True)
    is_active = models.BooleanField(verbose_name=_('Текущий граф'), default=False)
    mark = models.FloatField(verbose_name=_('Оценка графа'), null=True, blank=True)

    class Meta:
        verbose_name = l_('Граф пользователя')
        verbose_name_plural = l_('Графы пользователя')

    def __str__(self):
        return f'Граф пользователя {self.user} id {self.pk}'


class UserEmotion(models.Model):
    user = models.ForeignKey(User, related_name='emotions', verbose_name=_('Пользователь'), on_delete=models.CASCADE)
    file = models.FileField(verbose_name='файл эмоции',
                            upload_to=get_emotion_upload)

    class Meta:
        verbose_name = l_('Эмоция')
        verbose_name_plural = l_('Эмоции')

    def __str__(self):
        return f'Эмоция пользователя {self.user} файл {self.file}'
