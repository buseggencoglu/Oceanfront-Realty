# Generated by Django 3.1.4 on 2022-01-01 20:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oceanf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='birthDate',
            field=models.DateField(default=datetime.datetime(2022, 1, 1, 23, 31, 26, 408940)),
        ),
        migrations.AlterField(
            model_name='house',
            name='image',
            field=models.ImageField(blank=True, default='images/default', null=True, upload_to='house_images'),
        ),
    ]