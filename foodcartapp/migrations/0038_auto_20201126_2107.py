# Generated by Django 3.0.7 on 2020-11-26 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0037_auto_20201112_0105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer_first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='customer_last_name',
            new_name='lastname',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='phone_number',
            new_name='phonenumber',
        ),
    ]
