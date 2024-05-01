from rest_framework import serializers
from .models import ServiceRequest


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'
        read_only_fields = ('result',)

    def validate_latitude(self, value):
        """ Валидация широты: значение должно быть между -90 и 90. """
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("Широта должна быть в диапазоне от -90 до 90.")
        return value

    def validate_longitude(self, value):
        """ Валидация долготы: значение должно быть между -180 и 180. """
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("Долгота должна быть в диапазоне от -180 до 180.")
        return value