from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# مدل مشتری
class Customer(models.Model):
    phone_number = models.CharField(max_length=12, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)  # اختیاری
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} - {self.first_name or ''} {self.last_name or ''}"


# مدل لید (سرنخ فروش)
class Lead(models.Model):
    phone_number = models.CharField(max_length=12)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    source = models.CharField(
        max_length=100,
        choices=[
            ("website", _("وبسایت")),
            ("call", _("تماس تلفنی")),
            ("manual", _("دستی")),
        ],
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ("new", _("جدید")),
            ("contacted", _("تماس گرفته شده")),
            ("qualified", _("واجد شرایط")),
            ("lost", _("از دست رفته")),
        ],
        default="new",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} ({self.get_status_display()})"


# مدل تعاملات
class Interaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="interactions")
    type = models.CharField(
        max_length=50,
        choices=[
            ("call", _("تماس تلفنی")),
            ("sms", _("پیامک")),
            ("meeting", _("جلسه")),
            ("note", _("یادداشت")),
        ],
    )
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    interaction_date = models.DateTimeField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.get_type_display()} - {self.customer.phone_number}"


# مدل فرصت فروش
class Opportunity(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="opportunities")
    title = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    stage = models.CharField(
        max_length=50,
        choices=[
            ("prospecting", _("جستجو")),
            ("proposal", _("پیشنهاد")),
            ("negotiation", _("مذاکره")),
            ("won", _("برنده")),
            ("lost", _("بازنده")),
        ],
        default="prospecting",
    )
    expected_close_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.customer.phone_number}"


# مدل وظایف
class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", _("در انتظار")),
            ("in_progress", _("در حال انجام")),
            ("done", _("انجام شده")),
        ],
        default="pending",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    related_customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="tasks", blank=True, null=True
    )
    related_opportunity = models.ForeignKey(
        Opportunity, on_delete=models.CASCADE, related_name="tasks", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# مدل اسناد
class Document(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to="documents/")
    title = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# مدل برچسب‌ها
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    customers = models.ManyToManyField(Customer, related_name="tags", blank=True)

    def __str__(self):
        return self.name
