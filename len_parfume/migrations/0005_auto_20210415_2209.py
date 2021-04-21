# Generated by Django 3.1.7 on 2021-04-15 19:09

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('len_parfume', '0004_product_in_top'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image1',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='JPEG', keep_meta=True, quality=95, size=[800, 500], upload_to='images/photos/%Y/%m/%d/', verbose_name='Главное изображение'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image2',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, null=True, quality=95, size=[800, 500], upload_to='images/photos/%Y/%m/%d/', verbose_name='изображение 2'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image3',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, null=True, quality=95, size=[800, 500], upload_to='images/photos/%Y/%m/%d/', verbose_name='изображение 3'),
        ),
    ]
