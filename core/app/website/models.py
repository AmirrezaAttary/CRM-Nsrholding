from django.db import models
from django.utils import timezone
# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="title")
    image = models.ImageField(upload_to='news_images/', verbose_name="image", blank=True, null=True)
    content = models.TextField(verbose_name="content")
    author = models.CharField(max_length=100, verbose_name="author")
    tags = models.CharField(max_length=200, verbose_name="tags", help_text="Separate tags with commas")
    published_date = models.DateField(default=timezone.now, verbose_name="published date")
    is_active = models.BooleanField(default=True, verbose_name="is active")

    class Meta:
        verbose_name = "news"
        verbose_name_plural = "news"
        ordering = ['-published_date']

    def __str__(self):
        return self.title
    
class PurchaseLivestock (models.Model):
    product_name = models.CharField(max_length=100, verbose_name="product name")
    product_price = models.IntegerField(verbose_name="product price")
    product_description = models.TextField(verbose_name="product description")
    published_date = models.DateField(default=timezone.now, verbose_name="published date")
    product_photo = models.ImageField(verbose_name="product photo",null=True,blank=True)
    class Meta:
        verbose_name = "product"
        verbose_name_plural = "purchase livestock products"

    def __str__(self):
        return self.product_name
    
class OrganicProducts (models.Model):
    product_name = models.CharField(max_length=100, verbose_name="product name")
    published_date = models.DateField(default=timezone.now, verbose_name="published date")
    product_photo = models.ImageField(verbose_name="product photo",null=True,blank=True)
    product_title = models.TextField(verbose_name="product title")
    product_price = models.IntegerField(verbose_name="product price",default=0)
    class Meta:
        verbose_name = "product"
        verbose_name_plural = "organic products"

    def __str__(self):
        return self.product_name
    
class AnimalFeedKhoshab (models.Model):
    image = models.ImageField(verbose_name="image",null=True,blank=True)
    title = models.CharField(max_length=100, verbose_name='title')
    description = models.TextField(verbose_name="description")
    published_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "Animal Feed Khoshab"
    def __str__(self):
        return self.description

class MotherChickenFarm (models.Model):
    image = models.ImageField(verbose_name="image",null=True,blank=True)
    title = models.CharField(max_length=100, verbose_name='title')
    description = models.TextField(verbose_name="description")
    published_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "Mother Chicken Farm"
    def __str__(self):
        return self.description
    
class layingHen (models.Model):
    image = models.ImageField(verbose_name="image",null=True,blank=True)
    title = models.CharField(max_length=100, verbose_name='title')
    description = models.TextField(verbose_name="description")
    published_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "Laying Hen"
    def __str__(self):
        return self.description
    
class SupplyingLivestock (models.Model):
    image = models.ImageField(verbose_name="image",null=True,blank=True)
    title = models.CharField(max_length=100, verbose_name='title')
    description = models.TextField(verbose_name="description")
    published_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "Supplying Livestock"
    def __str__(self):
        return self.description
    
    
class AnimalRefinery (models.Model):
    image = models.ImageField(verbose_name="image",null=True,blank=True)
    title = models.CharField(max_length=100, verbose_name='title')
    description = models.TextField(verbose_name="description")
    published_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "Animal Refinery"
    def __str__(self):
        return self.description
    
class PlantRefinery (models.Model):
    image = models.ImageField(verbose_name="image",null=True,blank=True)
    title = models.CharField(max_length=100, verbose_name='title')
    description = models.TextField(verbose_name="description")
    published_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "Plant Refinery"
    def __str__(self):
        return self.description
    
class Contact (models.Model):
    full_name = models.CharField(max_length=100, verbose_name="full name")
    email = models.EmailField(verbose_name="email")
    number = models.CharField(verbose_name="mobile number",max_length=11)
    message = models.TextField(verbose_name="message")
    crate_deta = models.DateField(auto_now_add=True,verbose_name="sent time")

    class Meta:
        verbose_name = "Contact"
    
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

    name = models.CharField(max_length=100,verbose_name="full name")
    number = models.CharField(max_length=20,verbose_name="contact number")
    email = models.EmailField(verbose_name="email")
    city = models.CharField(max_length=100,verbose_name="city")
    job = models.CharField(max_length=50, choices=JOB_CHOICES,verbose_name="job")
    capital = models.CharField(max_length=100, choices=CAPITAL_CHOICES,verbose_name="capital")
    message = models.TextField(verbose_name="message")
    created_at = models.DateField(auto_now_add=True,verbose_name="sent time")

    def __str__(self):
        return f"{self.name} - {self.number}"