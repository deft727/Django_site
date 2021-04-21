from PIL import Image
from django.db import models
from django_resized import ResizedImageField
from django.urls import reverse
from django.contrib.auth import get_user_model
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid


User=get_user_model()



class Category(models.Model):

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['name',]

    name = models.CharField(max_length=250,verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug': self.slug})


class Size(models.Model):

    class Meta:
        verbose_name = 'Обьем'
        verbose_name_plural = 'Обьемы'
        ordering = ['size',]
    size = models.IntegerField(verbose_name='Объем')

    def __str__(self):
        return str(self.size)


class Product(models.Model):

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-pk',]

    category = models.ForeignKey(Category,on_delete=models.PROTECT,verbose_name='Категория продукта')
    title = models.CharField(max_length=250,db_index=True,verbose_name='Наименоватние продукта')
    slug=models.SlugField(unique=True)
    image1 = ResizedImageField(size=[800, 500],crop=['middle', 'center'],verbose_name='Главное изображение',quality=98, upload_to='images/photos/%Y/%m/%d/')
    image2 = ResizedImageField(size=[800, 500],crop=['middle', 'center'],blank=True,null=True,verbose_name='изображение 2',quality=98, upload_to='images/photos/%Y/%m/%d/')
    image3 = ResizedImageField(size=[800, 500],crop=['middle', 'center'],blank=True,null=True,verbose_name='изображение 3',quality=98, upload_to='images/photos/%Y/%m/%d/')
    features = models.ManyToManyField("specs.ProductFeatures", blank=True, related_name='features_for_product')
    sizes = models.ManyToManyField(Size,verbose_name='объемы', help_text="Выберите доступные Обьемы продукта")
    available = models.BooleanField(default=True,verbose_name="Наличие")
    description = models.TextField(verbose_name='Описание товара',null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Цена')
    old_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Старая Цена',null=True,blank=True)
    brand =  models.ImageField(verbose_name='Фото бренда если есть',upload_to='brands/photos/%Y/%m/%d/',null=True,blank=True)
    brand_name = models.CharField(max_length=50,verbose_name='Название бренда',null=True,blank=True)
    views = models.IntegerField (default=0,verbose_name='Кол-во просмотров')
    in_top = models.BooleanField(default=False,verbose_name="В новинках?")

    def get_absolute_url(self):
        return reverse('product_detail',kwargs={'slug': self.slug})
        
    def __str__(self):
        return self.title

    def get_features(self):
        return {f.feature.feature_name: ' '.join([f.value, f.feature.unit or ""]) for f in self.features.all()}

    # def save(self,*args,**kwargs):

    #     image1=self.image1
    #     if image1 :

    #         img1=Image.open(image1)
    #         new_img1=img1.convert('RGB')
    #         res_img1=new_img1
    #         # .resize((800,500),Image.ANTIALIAS)
    #         filestream= BytesIO()
    #         file_=res_img1.save(filestream,'JPEG',quality=90)
    #         filestream.seek(0)
    #         name= '{}.{}'.format(*self.image1.name.split('.'))
    #         self.image1 = InMemoryUploadedFile(
    #             filestream,'ImageFiedl',name,'jpeg/image',sys.getsizeof(filestream),  None
    #         )
    #         super().save(*args,**kwargs)
        
    #     image2=self.image2
    #     if image2 :

    #         img2=Image.open(image2)
    #         new_img2=img2.convert('RGB')
    #         res_img2=new_img2
    #         # .resize((600,500),Image.ANTIALIAS)
    #         filestream= BytesIO()
    #         file_=res_img2.save(filestream,'JPEG',quality=90)
    #         filestream.seek(0)
    #         name= '{}.{}'.format(*self.image2.name.split('.'))
    #         self.image2 = InMemoryUploadedFile(
    #             filestream,'ImageFiedl',name,'jpeg/image',sys.getsizeof(filestream),  None
    #         )
    #         super().save(*args,**kwargs)

    #     image3=self.image3
    #     if image3 :

    #         img3=Image.open(image3)
    #         new_img3=img3.convert('RGB')
    #         res_img3=new_img3
    #         # .resize((600,500),Image.ANTIALIAS)
    #         filestream= BytesIO()
    #         file_=res_img3.save(filestream,'JPEG',quality=90)
    #         filestream.seek(0)
    #         name= '{}.{}'.format(*self.image3.name.split('.'))
    #         self.image3 = InMemoryUploadedFile(
    #             filestream,'ImageFiedl',name,'jpeg/image',sys.getsizeof(filestream),  None
    #         )
    #         super().save(*args,**kwargs)
        

    #     brand=self.brand
    #     if brand :

    #         img3=Image.open(brand)
    #         new_img3=img3.convert('RGB')
    #         res_img3=new_img3.resize((130,100),Image.ANTIALIAS)
    #         filestream= BytesIO()
    #         file_=res_img3.save(filestream,'JPEG',quality=100)
    #         filestream.seek(0)
    #         name= '{}.{}'.format(*self.brand.name.split('.'))
    #         self.brand = InMemoryUploadedFile(
    #             filestream,'ImageFiedl',name,'jpeg/image',sys.getsizeof(filestream),  None
    #         )
    #         super().save(*args,**kwargs)



# class Tag(models.Model):
#     title = models.CharField(max_length=55,verbose_name='Название тега')
#     slug = models.SlugField(max_length=220,verbose_name='Url слага',unique=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name = 'Тег'
#         verbose_name_plural = 'Теги'
#         ordering = ['title']

#     def get_absolute_url(self):
#         return reverse('tag',kwargs={"slug":self.slug})




class Whishlist(models.Model):

    class Meta:
        verbose_name='Избранное'
        ordering = ['products',]
    owner = models.ForeignKey(User,null=True,  on_delete=models.CASCADE)
    session = models.CharField(max_length=200,null=True,blank=True)
    products = models.ForeignKey(Product,blank=True,related_name='Продукты',on_delete=models.CASCADE)
    whishlist = models.BooleanField(default=False,verbose_name="В избраном")

    def __str__(self):
        return  " Добавил: {} {} {}".format(self.id,str(self.owner),self.products)


class Customer(models.Model):

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')

    def __str__(self):
        return "Логин: {} , Покупатель: {} {}".format(self.user.username,self.user.first_name, self.user.last_name)



class Order(models.Model):

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    STATUS_NEW ='new'
    STATUS_IN_PROGRESS='in_progress'
    STATUS_READY= 'is_ready'
    STATUS_COMPLETED= 'completed'
    STATUS_DEACTIVE='deactive'

    BUYING_TYPE_SELF= 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES= (
        (STATUS_NEW,'Новый заказ'),
        (STATUS_IN_PROGRESS,'Заказ в обработке'),
        (STATUS_READY,'Заказ готов'),
        (STATUS_COMPLETED,'Заказ выполнен'),
        (STATUS_DEACTIVE,'Заказ Отменен')
    )

    BUYING_TYPE_CHOICES=(
        (BUYING_TYPE_SELF,'Отделение'),
        (BUYING_TYPE_DELIVERY,'Курьер')
        )

    PAY_TYPE_NAL = 'nal'
    PAY_TYPE_ONLINE='online'


    PAY_TYPE_CHOICES=(
        (PAY_TYPE_NAL,'Наложенный платеж'),
         (PAY_TYPE_ONLINE,'Онлайн оплата')
        )


    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    cartproduct = models.ManyToManyField('CartProduct', blank=True)
    final_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Общая сумма')
    email= models.EmailField(max_length=60, verbose_name='Емайл', null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон',help_text="+38-050-111-11-11")
    adress = models.CharField(max_length=60, verbose_name='Город', null=True, blank=True)
    otdel = models.CharField(max_length=20,verbose_name='Отделение', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказа',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Доставка',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    status_pay =  models.CharField(
        max_length=100,
        verbose_name='Оплата',
        choices=PAY_TYPE_CHOICES,
        default=PAY_TYPE_NAL
    )
    status_online = models.CharField(max_length=255, verbose_name='Статус онлайн оплаты',default='None', null=True, blank=True)
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')

    def __str__(self):
        return "Заказ: {} {} {}".format(self.id, self.first_name, self.last_name)



class CartProduct(models.Model):

    class Meta:
        verbose_name = 'Продукт для корзины'
        verbose_name_plural = 'Продукты для корзины'
        
    user  = models.ForeignKey('Customer',verbose_name='Покупатель', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,verbose_name='Товар',on_delete=models.CASCADE)
    size = models.CharField(max_length=150,verbose_name='объемы',null=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='сумма')
    
    def __str__(self):
        return "покупатель:{} объем: ({}) ,Продукт: {},Цена: {}".format(self.user,self.size,self.product.title,self.price)



class Rewiews(models.Model):

    name= models.CharField(max_length=255, verbose_name='Имя')
    text= models.TextField('Сообщение',max_length=500)
    product=models.ForeignKey(Product,verbose_name='Продукт',on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now=True,db_index=True,verbose_name='Добавлено')
    revId  = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return f"{self.name}-{self.product}"

    class Meta:
        verbose_name='Отзыв'
        verbose_name_plural='Отзывы'
        ordering = ['-data',]



class Likes(models.Model):

    class Meta:
        verbose_name='Лайк'
        verbose_name_plural='Лайки'

    post = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,verbose_name='Товар')
    like = models.BooleanField(default=False)
    liked_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True, verbose_name='Лайк от')