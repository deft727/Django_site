# Generated by Django 3.1.7 on 2021-04-19 17:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210415_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='postrewiews',
            name='postId',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
