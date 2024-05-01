import requests
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import time


@extend_schema(
    summary="Внешний сервер",
    description="Симуляция внешнего сервера с задержкой и выдачей случайного результата с отправкой "
                "обратно на внутренний сервер",
)
class SimulateExternalServerView(APIView):
    def post(self, request):
        settings.SIMULATE_STATUS = 'RUNNING'
        try:
            data = request.data
            time.sleep(random.randint(0, 60))
            result = random.choice([True, False])
            response_data = {
                'cad_num': data.get('cad_num'),
                'result': result
            }
            try:
                requests.post('http://localhost:8001/result/', json=response_data)
            except requests.RequestException as e:
                return Response({'error': str(e)}, status=500)
        finally:
            settings.SIMULATE_STATUS = 'IDLE'
