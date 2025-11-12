from django.db import models
from django.utils import timezone
# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان خبر")
    image = models.ImageField(upload_to='news_images/', verbose_name="تصویر خبر", blank=True, null=True)
    content = models.TextField(verbose_name="متن کامل خبر")
    author = models.CharField(max_length=100, verbose_name="نویسنده")
    tags = models.CharField(max_length=200, verbose_name="تگ‌ها", help_text="تگ‌ها را با کاما جدا کنید")
    published_date = models.DateField(default=timezone.now, verbose_name="تاریخ انتشار")
    is_active = models.BooleanField(default=True, verbose_name="نمایش داده شود؟")

    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "اخبار"
        ordering = ['-published_date']

    def __str__(self):
        return self.title
    
class PurchaseLivestock (models.Model):
    product_name = models.CharField(max_length=100, verbose_name="نام کالا")
    product_price = models.IntegerField(verbose_name="قیمت کالا")
    product_description = models.TextField(verbose_name="توضیحات کالا")
    published_date = models.DateField(default=timezone.now, verbose_name="تاریخ انتشار")
    product_photo = models.ImageField(verbose_name="عکس کالا",default='Default/DefaultImg.png',null=True,blank=True)
    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالا نهاد های دام"

    def __str__(self):
        return self.product_name
    
class OrganicProducts (models.Model):
    product_name = models.CharField(max_length=100, verbose_name="نام کالا")
    published_date = models.DateField(default=timezone.now, verbose_name="تاریخ انتشار")
    product_photo = models.ImageField(verbose_name="عکس کالا",default='Default/DefaultImg.png',null=True,blank=True)
    product_title = models.TextField(verbose_name="عنوان کالا")
    product_price = models.IntegerField(verbose_name="قیمت کالا",default=0)

    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "محصولات ارگانیک"

    def __str__(self):
        return self.product_name