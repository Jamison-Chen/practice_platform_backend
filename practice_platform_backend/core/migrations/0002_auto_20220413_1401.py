# Generated by Django 3.2 on 2022-04-13 06:01

from django.db import migrations, models
import practice_platform_backend.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='brand_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=practice_platform_backend.core.models.upload_to),
        ),
        migrations.AddField(
            model_name='tenant',
            name='tax_id_number',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='tel',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
