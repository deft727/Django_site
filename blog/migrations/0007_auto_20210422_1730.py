# Generated by Django 3.1.7 on 2021-04-22 14:30

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='JPEG', keep_meta=True, quality=90, size=[800, 446], upload_to='blog/photos/%Y/%m/%d/', verbose_name='Главное изображение'),
        ),
        migrations.AlterField(
            model_name='post',
            name='photo2',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='JPEG', keep_meta=True, quality=99, size=[1920, 786], upload_to='blog/photos/%Y/%m/%d/', verbose_name='изображение в топ'),
        ),
    ]
