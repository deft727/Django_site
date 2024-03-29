# Generated by Django 3.1.7 on 2021-06-03 19:52

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor.fields.RichTextField()),
                ('mini_text', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(upload_to='contact/')),
            ],
        ),
        migrations.AlterModelOptions(
            name='contactmodel',
            options={'verbose_name': 'Контакт', 'verbose_name_plural': 'Контакты'},
        ),
    ]
