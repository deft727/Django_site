# Generated by Django 3.1.7 on 2021-04-15 19:31

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo2',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], default=1, force_format='JPEG', keep_meta=True, quality=95, size=[1920, 786], upload_to='blog/photos/%Y/%m/%d/', verbose_name='изображение в топ'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='JPEG', keep_meta=True, quality=95, size=[800, 446], upload_to='blog/photos/%Y/%m/%d/', verbose_name='Главное изображение'),
        ),
    ]
