# Generated by Django 3.0.7 on 2021-02-15 19:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0052_auto_20210214_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='quantity',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
    ]
