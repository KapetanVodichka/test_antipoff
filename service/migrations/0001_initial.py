# Generated by Django 4.2.11 on 2024-05-01 22:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cad_num', models.CharField(unique=True, validators=[django.core.validators.RegexValidator(message='Кадастровый номер должен состоять из 8 цифр', regex='^\\d{8}$')], verbose_name='Кадастровый номер')),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=8, verbose_name='Широта')),
                ('longitude', models.DecimalField(decimal_places=5, max_digits=8, verbose_name='Долгота')),
                ('result', models.BooleanField(blank=True, null=True, verbose_name='Результат обработки')),
            ],
            options={
                'verbose_name': 'Запрос',
                'verbose_name_plural': 'Запросы',
            },
        ),
    ]
