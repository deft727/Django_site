from django.db import models
from django.urls import reverse
from PIL import Image
from django_resized import ResizedImageField
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.contrib.auth import get_user_model
from len_parfume.models import Customer
import uuid


User=get_user_model()


class CategoryBlog(models.Model):
    title = models.CharField(max_length=255,verbose_name='Название категории')
    slug = models.SlugField(max_length=220,verbose_name='Url категории',unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('categoryblog',kwargs={"slug":self.slug})


class Post(models.Model):

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']

    title = models.CharField(max_length=255,verbose_name='Название статьи')
    category = models.ForeignKey(CategoryBlog,on_delete=models.PROTECT,related_name='posts',verbose_name='Категория')
    slug = models.SlugField(max_length=220,verbose_name='slug статьи',unique=True)
    author = models.CharField(max_length=100,default='Админ',null=True,blank=True)
    preview = models.CharField(max_length=200,default='Какойто текст начала статьи',null=True,blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    photo = ResizedImageField(size=[800, 446],crop=['middle', 'center'],verbose_name='Главное изображение',quality=90,upload_to='blog/photos/%Y/%m/%d/')
    photo2 = ResizedImageField(size=[1920, 786],crop=['middle', 'center'],verbose_name='изображение в топ',quality=99,upload_to='blog/photos/%Y/%m/%d/')
    views = models.IntegerField (default=0,verbose_name='Кол-во просмотров')
    is_publish = models.BooleanField(default=True,verbose_name='Публиковать?')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post',kwargs={"slug":self.slug})


    # def save(self,*args,**kwargs):

    #     photo=self.photo
    #     if photo :
    #         img1=Image.open(photo)
    #         new_img1=img1.convert('RGB')
    #         res_img1=new_img1
    #         filestream= BytesIO()
    #         file_=res_img1.save(filestream,'JPEG',quality=90)
    #         filestream.seek(0)
    #         name= '{}.{}'.format(*self.photo.name.split('.'))
    #         self.photo = InMemoryUploadedFile(
    #             filestream,'ImageFiedl',name,'jpeg/image',sys.getsizeof(filestream),  None
    #         )
    #         super().save(*args,**kwargs)





class PostRewiews(models.Model):

    name= models.CharField(max_length=255, verbose_name='Имя')
    text= models.TextField('Сообщение',max_length=1000,help_text='Максимум 1000 символов')
    post=models.ForeignKey(Post,verbose_name='Пост',on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True,db_index=True,verbose_name='Добавлено')
    postId  = models.UUIDField(default=uuid.uuid4)
    def __str__(self):
        return f"{self.name}-{self.post}"

    class Meta:
        verbose_name='Отзыв'
        verbose_name_plural='Отзывы Блога'
        ordering=('-data',)

    

