# Generated by Django 3.1.7 on 2021-06-03 19:17

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название магазина')),
                ('email', models.EmailField(max_length=254, verbose_name='Эмайл')),
                ('developer', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Эмайл разработчика')),
                ('text', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(upload_to='contact/')),
            ],
        ),
        migrations.CreateModel(
            name='ContactQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Введите E-mail')),
                ('message', models.TextField(max_length=5000, verbose_name='Введите сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'ordering': ['-created_at'],
            },
        ),
    ]