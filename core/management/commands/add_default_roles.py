from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from core.models import Role


class Command(BaseCommand):
    """
    Команда для создания роли пользователь.
    """

    def handle(self, *args, **options):
        # Создаем роль обычного пользователя
        role_user_student, created = Role.objects.get_or_create(name='Ученик', slug='student', defaults={'rank': 0})
        role_user_teacher, created = Role.objects.get_or_create(name='Учитель', slug='teacher', defaults={'rank': 0})

        role_user_student.permissions.add(Permission.objects.get_by_natural_key('switch_company', 'core', 'user'))
        role_user_teacher.permissions.add(Permission.objects.get_by_natural_key('switch_company', 'core', 'user'))
