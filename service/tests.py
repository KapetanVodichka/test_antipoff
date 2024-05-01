from decimal import Decimal
from .models import ServiceRequest
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class ServiceRequestTests(APITestCase):
    def setUp(self):
        # Подготовка тестовых данных
        self.test_data = {
            'cad_num': '12345678',
            'latitude': 34.05223,
            'longitude': -118.24368
        }

    def test_full_interaction(self):
        # Запрос на /query
        request_response = self.client.post(
            reverse('service:query'),
            data=self.test_data,
            format='json'
        )

        # Проверка сохранения отправленного запроса в БД
        request_obj = ServiceRequest.objects.get(cad_num='12345678')
        self.assertIsNotNone(request_obj)
        self.assertEqual(request_obj.cad_num, '12345678')
        self.assertEqual(request_obj.latitude, Decimal('34.05223'))
        self.assertEqual(request_obj.longitude, Decimal('-118.24368'))
        self.assertEqual(request_obj.result, None)

        # Через сваггер запрос на /query сразу делает запрос на внешний сервер /simulate и оттуда идет
        # запрос на /result, но в тестах почему-то запрос на /result не идет, поэтому делаем симуляцию запроса /result
        result_response = self.client.post(
            reverse('service:result'),
            {'cad_num': '12345678', 'result': True},
            format='json'
        )
        self.assertEqual(result_response.status_code, status.HTTP_200_OK)
        # Проверка сохранения результата запроса в БД
        request_obj = ServiceRequest.objects.get(cad_num='12345678')
        self.assertEqual(request_obj.result, True)
