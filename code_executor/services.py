import json
import logging
from django.utils.translation import gettext as _
import requests
from django.conf import settings
from .models import ExecuteCodeLog

LOG = logging.getLogger(__name__)


class CodeExecuteException(Exception):
    pass


class CodeExecutorService(object):
    PYTHON = 1
    AVAILABLE_SANDBOX = {
        PYTHON: {
            'name': 'Python',
            'template': 'templates/code_executor/telegram_template.py'
        },
    }
    ERROR_MESSAGES = {
        'execute_time_excepted': _('Доступное время для запуска кода израсходовано'),
        'request_error': _('Ошибка при отправке запроса'),
        'unknown_error': _('Неизвестная ошибка с песочницей'),
    }

    def get_template(self):
        return self.AVAILABLE_SANDBOX[self.executor]['template']

    def check_user_available_time(self):
        return self.user.execute_settings.available_time > 0

    def __init__(self, code: str, user, executor: int = PYTHON):
        self.code = code
        self.user = user
        self.executor = executor

    def _render_template(self):
        template = self.get_template()
        return template.format(self.code)

    def run_code(self):
        if not self.check_user_available_time():
            raise CodeExecuteException(self.ERROR_MESSAGES['execute_time_excepted'])
        code = self._render_template()
        data = {
            "auth_key": settings.EXECUTOR_AUTH_KEY,
            "user_id": self.user.id,
            "available_time": self.user.execute_settings.available_time,
            "code": code
        }
        execute_log = ExecuteCodeLog(user=self.user, request=json.dumps(data))
        try:
            response = requests.post(f'{settings.EXECUTOR_BASE_URL}/api/execute', json=data)
            execute_log.response = response.text
            if not response.ok:
                execute_log.status = False
                execute_log.save()
                try:
                    response_data = response.json()
                    raise CodeExecuteException(
                        response_data.get('error', self.ERROR_MESSAGES['unknown_error'])
                    )
                except json.JSONDecodeError:
                    raise CodeExecuteException(self.ERROR_MESSAGES['unknown_error'])
            execute_log.save()
        except requests.RequestException as e:
            LOG.exception(e)
            execute_log.error = str(e)
            raise CodeExecuteException(self.ERROR_MESSAGES['request_error'])
