from typing import Union


class CodeExecutorService(object):
    PYTHON = 1
    AVAILABLE_SANDBOX = {
        PYTHON: {
            'name': 'Python',
            'template': 'templates/code_executor/telegram_template.py'
        },
    }

    def get_template(self):
        return self.AVAILABLE_SANDBOX[self.executor]['template']

    def __init__(self, code: str, executor: int = PYTHON):
        self.code = code
        self.executor = executor

    def _render_template(self):
        template = self.get_template()
        return template.format(self.code)

    def run_code(self):
        code = self._render_template()
        # TODO: реализовать запрос к песочнице
        return False
