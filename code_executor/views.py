from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from core.models import User
from .models import UserExecuteSettings
from .serializers import ExecuteCodeSerializer, ConsoleLogSerializer
from .services import CodeExecutorService, CodeExecuteException
from rest_framework.permissions import IsAuthenticated


class ExecuteCodeView(APIView):
    serializer_class = ExecuteCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = ExecuteCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.data['code']
            try:
                executor_service = CodeExecutorService(code, self.request.user)
                executor_service.run_code()
            except CodeExecuteException as e:
                return Response({'success': False, 'errors': {'common': str(e)}})
            return Response({'success': True, 'message': 'Код запущен'})
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ConsoleCallbackView(APIView):

    serializer = ConsoleLogSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            execute_settings = request.user.execute_settings
            ser = self.serializer(execute_settings)
            return Response({'success': True, 'data': ser.data})
        except UserExecuteSettings.DoesNotExist:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
