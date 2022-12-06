from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.translation import gettext_lazy as l_


class Role(models.Model):
    name = models.CharField(
        l_('Наименование'),
        max_length=80)

    slug = models.SlugField(
        l_('Кодовое имя'),
        max_length=80,
        unique=True)

    permissions = models.ManyToManyField(
        Permission,
        verbose_name=l_('Права'),
        blank=True)

    rank = models.PositiveSmallIntegerField(
        l_('Уровень'),
        blank=True,
        default=0,
        help_text=l_('Уровень роли, чем выше число, тем выше '
                     'уровень роли по отношению к другим ролям'))

    class Meta:
        verbose_name = l_('Роль')
        verbose_name_plural = l_('Роли')

    def __str__(self):
        return self.name


class User(AbstractUser):
    roles = models.ManyToManyField('Role', verbose_name=l_('Роли'), blank=True, related_name='users')
    birth_date = models.DateField(verbose_name=l_('Дата рождения'), blank=True, null=True)

    class Meta:
        verbose_name = l_('Пользователь')
        verbose_name_plural = l_('Пользователи')

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.username

    def get_my_teacher(self):
        return Teacher.objects.filter(student_group__pk__in=self.pk).first()

    def is_teacher(self):
        try:
            return bool(self.teacher)
        except:
            return False

    def is_student(self):
        try:
            return not bool(self.teacher)
        except:
            return True


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher',
                                verbose_name=l_(u'Пользователь'))
    student_group = models.ManyToManyField(User, related_name='teachers', verbose_name=l_('Класс'))

    class Meta:
        verbose_name = l_('Учитель')
        verbose_name_plural = l_('Учителя')


