from rest_framework import viewsets
from .models import UserGraphConstructor
from .serializers import UserGraphConstructorSerializer


class GraphConstructorViewSet(viewsets.ModelViewSet):
    queryset = UserGraphConstructor.objects.all()
    serializer_class = UserGraphConstructorSerializer
    # TODO: добавить права для доступа
    permission_classes = []

    def get_queryset(self):
        qs = super(GraphConstructorViewSet, self).get_queryset()
        return qs.filter(user=self.request.user).order_by('is_active')
