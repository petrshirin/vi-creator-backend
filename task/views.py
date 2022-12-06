from rest_framework import viewsets, permissions, views, status
from .models import Task, UserAnswer
from .serializers import TaskSerializer, TaskTeacherSerializer, \
    UserAnswerSerializer, UserAnswerPostSerializer, TeacherUserAnswerSerializer
from .permissions import IsCanEditTaskOrReadOnly, IsCanMakeAnswerOrReadOnly


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsCanEditTaskOrReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_teacher():
            return TaskTeacherSerializer
        return TaskSerializer

    def get_queryset(self):
        qs = super(TaskViewSet, self).get_queryset()
        if self.request.user.is_teacher():
            return qs.for_teacher(self.request.user)
        return qs.for_student(self.request.user)

    def perform_create(self, serializer: TaskTeacherSerializer):
        serializer.instance.teacher = self.request.user.teacher
        return super(TaskViewSet, self).perform_create(serializer)


class StudentAnswerApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsCanMakeAnswerOrReadOnly]

    def has_user_access(self, obj):
        if self.request.user.is_student():
            return obj.teacher.student_group.filter(username=self.request.user.username).exists()
        else:
            return self.request.user.teacher == obj.teacher

    def get_object(self, task_id):
        return Task.objects.get(pk=task_id)

    def get(self, request):
        try:
            obj = self.get_object(self.request.data.get('id'))
        except Task.DoesNotExist:
            return views.Response({'success': False, 'obj': None}, status=status.HTTP_404_NOT_FOUND)
        if self.has_user_access(obj):
            if request.user.is_student():
                ser = UserAnswerSerializer(obj)
            else:
                ser = TeacherUserAnswerSerializer(obj)
            return views.Response({'success': True, 'obj': ser.data})
        return views.Response({'success': True, 'obj': None}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            obj = self.get_object(request.data.get('id'))
        except Task.DoesNotExist:
            obj = None
        if not obj or self.has_user_access(obj):
            if request.user.is_student():
                ser = UserAnswerPostSerializer(obj, data=request.data)
                if not ser.is_valid():
                    return views.Response({'success': False, 'errors': ser.errors},
                                          status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                ser.instance.status = UserAnswer.ON_CHECKING
                ser.save()
                return views.Response({'success': True, 'obj': UserAnswerSerializer(ser.instance).data},
                                      status=status.HTTP_201_CREATED)
