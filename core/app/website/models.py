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
    product_photo = models.ImageField(verbose_name="عکس کالا",null=True,blank=True)
    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالا نهاد های دام"

    def __str__(self):
        return self.product_name
    
class OrganicProducts (models.Model):
    product_name = models.CharField(max_length=100, verbose_name="نام کالا")
    published_date = models.DateField(default=timezone.now, verbose_name="تاریخ انتشار")
    product_photo = models.ImageField(verbose_name="عکس کالا",null=True,blank=True)
    product_title = models.TextField(verbose_name="عنوان کالا")
    product_price = models.IntegerField(verbose_name="قیمت کالا",default=0)

    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "محصولات ارگانیک"

    def __str__(self):
        return self.product_name
    
class AnimalFeedKhoshab (models.Model):
    image = models.ImageField(verbose_name="عکس",null=True,blank=True)
    title = models.CharField(max_length=100, verbose_name='عنوان')
    description = models.TextField(verbose_name="عنوان")
    published_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "خوراک دام خوشاب"

    def __str__(self):
        return self.description

class MotherChickenFarm (models.Model):
    image = models.ImageField(verbose_name="عکس",null=True,blank=True)
    title = models.CharField(max_length=100, verbose_name='عنوان')
    description = models.TextField(verbose_name="عنوان")
    published_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "مزرعه مرغ مادر"

    def __str__(self):
        return self.description
    
class layingHen (models.Model):
    image = models.ImageField(verbose_name="عکس",null=True,blank=True)
    title = models.CharField(max_length=100, verbose_name='عنوان')
    description = models.TextField(verbose_name="عنوان")
    published_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "مجموعه مرغ تخم گذار"

    def __str__(self):
        return self.description
    
class SupplyingLivestock (models.Model):
    image = models.ImageField(verbose_name="عکس",null=True,blank=True)
    title = models.CharField(max_length=100, verbose_name='عنوان')
    description = models.TextField(verbose_name="عنوان")
    published_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "تامبن نهاد های دامی"

    def __str__(self):
        return self.description
    
    
class AnimalRefinery (models.Model):
    image = models.ImageField(verbose_name="عکس",null=True,blank=True)
    title = models.CharField(max_length=100, verbose_name='عنوان')
    description = models.TextField(verbose_name="عنوان")
    published_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "پالیشگاه دام"

    def __str__(self):
        return self.description
    
class PlantRefinery (models.Model):
    image = models.ImageField(verbose_name="عکس",null=True,blank=True)
    title = models.CharField(max_length=100, verbose_name='عنوان')
    description = models.TextField(verbose_name="عنوان")
    published_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "پالیشگاه گیاهان دارویی"

    def __str__(self):
        return self.description
    
class Contact (models.Model):
    full_name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(verbose_name="ایمیل")
    number = models.CharField(verbose_name="شماره موبایل",max_length=11)
    message = models.TextField(verbose_name="پیام")
    crate_deta = models.DateField(auto_now_add=True,verbose_name="زمان ارسال")

    class Meta:
        verbose_name = "تماس با ما"
    
    def __str__(self):
        return self.full_name
    
class ContactRequest(models.Model):
    JOB_CHOICES = [
        ("آزاد", "آزاد"),
        ("بیکار", "بیکار"),
        ("کارمند", "کارمند"),
        ("بازنشسته", "بازنشسته"),
        ("دیگر مشاغل", "دیگر مشاغل"),
    ]

    CAPITAL_CHOICES = [
        ("کمتر از 200 میلیون تومان", "کمتر از 200 میلیون تومان"),
        ("بین 200 تا 500 میلیون تومان", "بین 200 تا 500 میلیون تومان"),
        ("بین 500 میلیون تومان تا یک میلیارد تومان", "بین 500 میلیون تومان تا یک میلیارد تومان"),
        ("بیشتر از یک میلیارد تومان", "بیشتر از یک میلیارد تومان"),
    ]

    name = models.CharField(max_length=100,verbose_name="نام و نام خانوادگی")
    number = models.CharField(max_length=20,verbose_name="شماره تماس")
    email = models.EmailField(verbose_name="ایمیل")
    city = models.CharField(max_length=100,verbose_name="شهر")
    job = models.CharField(max_length=50, choices=JOB_CHOICES,verbose_name="شغل")
    capital = models.CharField(max_length=100, choices=CAPITAL_CHOICES,verbose_name="میزان سرمایه")
    message = models.TextField(verbose_name="پیام مورد نظر")
    created_at = models.DateField(auto_now_add=True,verbose_name="زمان ارسال")

    def __str__(self):
        return f"{self.name} - {self.number}"