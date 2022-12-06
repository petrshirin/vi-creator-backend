from rest_framework import viewsets, views, permissions, status
from .models import UserGraphConstructor, UserEmotion
from .serializers import UserGraphConstructorSerializer, SetActiveGraphSerializer


class GraphConstructorViewSet(viewsets.ModelViewSet):
    queryset = UserGraphConstructor.objects.all()
    serializer_class = UserGraphConstructorSerializer
    # TODO: добавить права для доступа
    permission_classes = []

    def get_queryset(self):
        qs = super(GraphConstructorViewSet, self).get_queryset()
        return qs.filter(user=self.request.user).order_by('is_active')


class UserEmotionViewSet(viewsets.ModelViewSet):
    queryset = UserEmotion.objects.all()
    serializer_class = None

    def get_queryset(self):
        qs = super(UserEmotionViewSet, self).get_queryset()
        return qs.filter(user=self.request.user)


class ActiveGraphView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    get_serializer_class = SetActiveGraphSerializer
    post_serializer_class = UserGraphConstructorSerializer

    def get_object(self):
        return UserGraphConstructor.objects.filter(user=self.request.user, is_active=True)

    def get(self, request):
        obj = self.get_object()
        return views.Response({
            'success': True,
            'data': self.get_serializer_class(obj).data
        })

    def post(self, request):
        serializer = self.post_serializer_class(data=request.data)
        if serializer.is_valid():
            obj: UserGraphConstructor = serializer.instance
            UserGraphConstructor.objects.filter(user=self.request.user,
                                                is_active=True).update(is_active=False)
            obj.is_active = True
            obj.save()
            return views.Response({
                'success': True,
                'data': self.get_serializer_class(obj).data
            }, status=status.HTTP_201_CREATED)
        return views.Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
