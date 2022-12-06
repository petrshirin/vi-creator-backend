from django.db import models
from task.models import Teacher


class TaskManager(models.Manager):

    def get_queryset(self):
        qs = super(TaskManager, self).get_queryset()
        return qs.filter()

    def for_student(self, user):
        user_teachers = Teacher.objects.filter(student_group__exact=user)
        return self.get_queryset().filter(teacher__in=user_teachers)

    def for_teacher(self, user):
        return self.get_queryset().filter(teacher=user.teacher)
