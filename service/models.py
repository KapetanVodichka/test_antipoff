from django.core.validators import RegexValidator
from django.db import models


class ServiceRequest(models.Model):
    cad_num = models.CharField(
        verbose_name='Кадастровый номер',
        unique=True,
        validators=[
            RegexValidator(
                regex='^\\d{8}$',
                message="Кадастровый номер должен состоять из 8 цифр"
            )
        ]
    )
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        verbose_name='Широта'
    )
    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        verbose_name='Долгота'
    )
    result = models.BooleanField(
        null=True, blank=True,
        verbose_name='Результат обработки'
    )

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
        app_label = 'service'

    def __str__(self):
        return f"Запрос {self.cad_num} с координатами {self.latitude}, {self.longitude}"