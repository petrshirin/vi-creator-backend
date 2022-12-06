# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
import requests
from core.models import User
from .models import UserExecuteSettings
from core.utils.utils import batch_generator
from django.conf import settings
from vi_creator_backend.celery import app as celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def get_containers_logs():
    user_ids = User.objects.filter(
        teacher__isnull=False,
        is_staff=False
    ).values_list('id', flat=True)

    for batch in batch_generator(user_ids, 50):
        request_data = {
            'auth_key': settings.EXECUTOR_AUTH_KEY,
            'user_ids': batch,
        }
        response = requests.post(
            f'{settings.EXECUTOR_BASE_URL}/logs/',
            json=request_data
        )
        if response.ok:
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                logger.error(e)
                continue
            objects_to_update = {
                obj.user_id: obj
                for obj in UserExecuteSettings.objects.filter(
                    pk__in=list(map(lambda i: int(i['user_id']), data))
                )
            }
            for log_data in data:
                objects_to_update[log_data['user_id']].console_content = log_data['logs']
            count = UserExecuteSettings.objects.bulk_update(
                objects_to_update.values(),
                ['console_content']
            )
            logger.info(f'Обновлены логи консоли для {count} пользователей')
        else:
            logger.error(f'Ошибка при запросе к логам request: '
                         f'{request_data}, response: {response.text}')
