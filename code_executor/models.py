from django.db import models
from django.utils.translation import gettext_lazy as l_
from django.conf import settings


class ExecuteCodeLog(models.Model):
    user = models.ForeignKey('core.User', verbose_name=l_('Пользователь'), on_delete=models.CASCADE)
    date_started = models.DateTimeField(auto_now_add=True, verbose_name=l_('Дата создания'))
    error = models.TextField(verbose_name=l_('Ошибка'), null=True, blank=True)
    request = models.TextField(verbose_name=l_('Запрос'), null=True, blank=True)
    response = models.TextField(verbose_name=l_('Ответ'), null=True, blank=True)
    status = models.BooleanField(verbose_name=l_('Статус запроса'), default=True)

    class Meta:
        verbose_name = l_('Лог запуска кода')
        verbose_name_plural = l_('Логи запуска кода')


class UserExecuteSettings(models.Model):
    user = models.OneToOneField('core.User', verbose_name=l_('Пользователь'),
                                on_delete=models.CASCADE, related_name='execute_settings')
    available_time = models.FloatField(verbose_name=l_('Оставшееся время работы в секундах'),
                                       default=settings.EXECUTE_DEFAULT_TIME)
    console_content = models.TextField(verbose_name=l_('Последний вывод консоли'),
                                       default=None, null=True, blank=True)

    class Meta:
        verbose_name = l_('Настройки запуска кода пользователя')
        verbose_name_plural = l_('Настройки запуска кода пользователей')
