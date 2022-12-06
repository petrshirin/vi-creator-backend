from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from core.models import User
from core.serializers import RegisterSerializer, UserSerializer
from core.utils.permissions import IsNotAuthenticated, IsTeacher
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.db import transaction
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsNotAuthenticated,)
    serializer_class = RegisterSerializer
    token_serializer_class = AuthTokenSerializer

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response({'token': token.key, 'success': True}, status=status.HTTP_201_CREATED, headers=headers)


class MyStudentView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user.teacher.student_group.all()


class MyUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = super(MyUserView, self).get_queryset()
        if self.request.user.is_authenticated:
            return qs.filter(pk=self.request.user.pk)
