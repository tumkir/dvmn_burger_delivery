# Generated by Django 3.0.7 on 2021-02-21 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0055_auto_20210217_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='address',
            field=models.CharField(max_length=500, unique=True, verbose_name='Адрес'),
        ),
    ]
