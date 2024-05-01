import requests
from django.conf import settings
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ServiceRequest
from .serializers import ServiceRequestSerializer


@extend_schema(
    summary="Отправка нового запроса на внешний сервер",
    description="Принимает кадастровый номер, широту и долготу, и отправляет эти данные на внешний сервер ",
    request=ServiceRequestSerializer,
    responses={201: ServiceRequestSerializer}
)
class QueryView(APIView):
    def post(self, request):
        serializer = ServiceRequestSerializer(data=request.data)
        if serializer.is_valid():
            request_obj = serializer.save()
            data = {
                'cad_num': request_obj.cad_num,
                'latitude': float(request_obj.latitude),
                'longitude': float(request_obj.longitude)
            }
            requests.post('http://localhost:8001/simulate/', json=data)
            return Response({"message": "Запрос получен и был отправлен на внешний сервер"}, status=202)
        return Response(serializer.errors, status=400)


@extend_schema(
    summary="Обновление результата запроса",
    description="Обновляет результат конкретного запроса, идентифицированного по ID, указывая, что "
                "он был обработан внешним сервером.",
)
class ResultView(APIView):
    def post(self, request):
        cad_num = request.data.get('cad_num')
        result = request.data.get('result')
        try:
            request_obj = ServiceRequest.objects.get(cad_num=cad_num)
            request_obj.result = result
            request_obj.save()
            serializer = ServiceRequestSerializer(request_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ServiceRequest.DoesNotExist:
            return Response({"error": "Запрос с данным кадастровым номером не найден"},
                            status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    summary="Проверка состояния сервера",
    description="Предоставляет простой способ проверки работоспособности сервера.",
    responses={200: {'description': 'Сервер работает'}}
)
class PingView(APIView):
    def get(self, request):
        if getattr(settings, 'SIMULATE_STATUS', 'IDLE') == 'RUNNING':
            return Response({"message": "Внешний сервер /simulate работает"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Внешний сервер /simulate не работает"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)


@extend_schema(
    summary="Получение истории всех запросов",
    description="Получает историю всех запросов или фильтрует по кадастровому номеру, если он указан.",
    parameters=[
        OpenApiParameter(
            name='cad_num',
            type=OpenApiTypes.STR,
            description="Кадастровый номер для фильтрации запросов",
        )
    ],
    responses={200: ServiceRequestSerializer(many=True)}
)
class HistoryView(APIView):
    def get(self, request):
        cad_num = request.query_params.get('cad_num')
        if cad_num:
            requests = ServiceRequest.objects.filter(cad_num=cad_num)
        else:
            requests = ServiceRequest.objects.all()
        serializer = ServiceRequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
