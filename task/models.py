from django.db import models
from core.models import Teacher, User
from django.utils.translation import gettext_lazy as l_, gettext as _


class Task(models.Model):
    GRAPH = 1
    MANUAL = 2
    SIMPLE_ANSWER = 3
    TYPES = (
        (GRAPH, _('Задание на граф')),
        (MANUAL, _('Ручная проверка')),
        (SIMPLE_ANSWER, _('Простой ответ')),
    )

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=l_('Учитель'))
    name = models.CharField(max_length=255, verbose_name=l_('Название'))
    description = models.TextField(verbose_name=l_('Описание'))
    type = models.PositiveSmallIntegerField(verbose_name=l_('Тип задания'), default=SIMPLE_ANSWER, choices=TYPES)
    auto_check = models.BooleanField(verbose_name=l_('Автоматическая проверка'),
                                     help_text=l_('Автоматическая проверка доступна только для графа'))
    answer = models.CharField(verbose_name='Ответ на задание', null=True, blank=True, max_length=512)
    graph_answer = models.ForeignKey('graph_constructor.UserGraphConstructor',  on_delete=models.SET_NULL,
                                     null=True, blank=True, verbose_name=l_('Проверочный граф'))
    max_mark = models.FloatField(verbose_name=l_('Оценка за задание'))

    class Meta:
        verbose_name = l_('Задание')
        verbose_name_plural = l_('Задания')

    def __str__(self):
        return self.name


class UserAnswer(models.Model):
    NONE = 0
    ON_CHECKING = 1
    COMPLETED = 2

    STATUSES = (
        (NONE, _('Нет ответа')),
        (ON_CHECKING, _('На проверке')),
        (COMPLETED, _('Завершено')),
    )

    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name=l_('Ответ на задание'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=l_('Пользователь'))
    answer = models.CharField(verbose_name='Ответ на задание', null=True, blank=True, max_length=512)
    answer_graph = models.ForeignKey('graph_constructor.UserGraphConstructor',  on_delete=models.SET_NULL,
                                     null=True, blank=True, verbose_name=l_('ответ в виде графа'))
    mark = models.FloatField(verbose_name=l_('Оценка'), null=True, blank=True, default=None)
    status = models.PositiveSmallIntegerField(verbose_name=l_('Статус ответа'), choices=STATUSES, default=NONE)

    class Meta:
        verbose_name = l_('Ответ пользователя')
        verbose_name_plural = l_('Ответы пользователей')

    def __str__(self):
        return _('Ответ пользователя {} на задание {}').format(self.user, self.task)
