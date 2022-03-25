# Generated by Django 3.2 on 2022-03-25 04:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tenant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('domain_name', models.CharField(max_length=256, unique=True)),
                ('schema_name', models.CharField(max_length=1024, unique=True)),
            ],
        ),
    ]
