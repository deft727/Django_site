from django import VERSION
from django.db import models
from ckeditor.fields import RichTextField


class ContactModel(models.Model):
    """класс модели контактов"""
    name = models.CharField(verbose_name='Название магазина',max_length=200)
    email = models.EmailField(verbose_name='Эмайл')
    developer = models.EmailField(blank=True,null=True,verbose_name='Эмайл разработчика')
    text = RichTextField()
    image = models.ImageField(upload_to="contact/")
    
    class Meta:
        verbose_name='Контакт'
        verbose_name_plural='Контакты'

    def __str__(self):
        return f'{self.email}'

class ContactQuestions(models.Model):
    email = models.EmailField(verbose_name='Введите E-mail')
    message = models.TextField(max_length=5000,verbose_name='Введите сообщение')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name='Вопрос'
        verbose_name_plural='Вопросы'
        ordering = ["-created_at",]

    def __str__(self) -> str:
        return self.email


class AboutModel(models.Model):
    ''' класс модели страницы о нас '''
    mini_text = RichTextField()
    text = RichTextField()
    image = models.ImageField(upload_to="contact/")

    class Meta:
        verbose_name = "О нас"

    def __str__(self):
        return self.mini_text


class FaqModel(models.Model):
    ''' класс информационной модели'''
    question = models.CharField(max_length=250,verbose_name='Вопрос')
    answer = models.CharField(max_length=500,verbose_name='Ответ')

    class Meta:
        verbose_name = 'Часто задаваемые вопросы'

    def __str__(self) -> str:
        return self.question


class Social(models.Model):
    ''' класс модели соц сетей'''
    # icon = models.FileField(upload_to="icons/")
    name = models.CharField(max_length=200)
    link = models.URLField()

    class Meta:
        verbose_name = 'Социальные сети'

    def __str__(self) -> str:
        return self.name


class FooterInfo(models.Model):
    title = models.CharField(max_length=200,verbose_name='Название магазина')
    adress = models.CharField(max_length=200,verbose_name='Адресс')
    phone = models.CharField(max_length=200,verbose_name='Телефон')
    email = models.EmailField(verbose_name='Введите E-mail')

    class Meta:
        verbose_name = 'Инфо в футер'

    def __str__(self):
        return self.title


# class ContactLink(models.Model):
#     ''' Класс модели контактов'''
#     icon = models.FileField(upload_to="icons/")
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name





# class ImageAbout(models.Model):
#     '''Класс модели изображений  о нас '''
#     image = models.ImageField(upload_to="about/")
#     page = models.ForeignKey(About,on_delete=models.CASCADE,related_name='about_images')
#     alt = models.CharField(max_length=200)


# class Social(models.Model):
#     ''' класс модели соц сетей'''
#     icon = models.FileField(upload_to="icons/")
#     name = models.CharField(max_length=200)
#     link = models.URLField()

#     def __str__(self) -> str:
#         return self.name
