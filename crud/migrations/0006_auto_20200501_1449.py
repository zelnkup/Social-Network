# Generated by Django 2.2 on 2020-05-01 14:49

import crud.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0005_auto_20200501_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='token',
            field=models.CharField(default=crud.models.gen_token, max_length=10, unique=True),
        ),
    ]