from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer, TaskTeacherSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # TODO: добавить права для доступа
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.teacher:
            return TaskTeacherSerializer
        return TaskSerializer

    def get_queryset(self):
        qs = super(TaskViewSet, self).get_queryset()
        # TODO: Добавить логику получения заданий
        return qs

    def perform_create(self, serializer: TaskSerializer):
        serializer.instance.teacher = self.request.user.teacher
        return super(TaskViewSet, self).perform_create(serializer)
