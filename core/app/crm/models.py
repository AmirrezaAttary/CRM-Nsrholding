from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jmodels


# model FieldActivity
class FieldActivity(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Activity Name"))
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_("Parent Activity")
    )

    class Meta:
        verbose_name = _("Field Activity")
        verbose_name_plural = _("Field Activities")

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

# model ValidationLevel
class ValidationLevel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Validation Name"))
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_("Parent Validation")
    )

    class Meta:
        verbose_name = _("Validation Level")
        verbose_name_plural = _("Validation Levels")

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name


# model CallReport
class CallReport (models.Model):

    number = models.CharField(max_length=20, verbose_name=_("Phone Number"), blank=True, null=True)

    name = models.CharField (max_length=255, verbose_name=_("Name"),blank=True, null=True)

    field_activity = models.ForeignKey(
    FieldActivity,
    on_delete=models.PROTECT,  
    null=True,
    blank=True,
    verbose_name=_("Field of Activity"),
    related_name='call_reports'
    )

    province = models.CharField (max_length=255, verbose_name=_("Province"),blank=True, null=True)
    city = models.CharField (max_length=255, verbose_name=_("City"),blank=True, null=True)

    last_purchase = jmodels.jDateField (verbose_name=_("Last Purchase"),blank=True, null=True)
    purchase_satisfaction = models.BooleanField (verbose_name=_("Purchase Satisfaction"),default=False, blank=True)

    validation = models.ForeignKey(
        ValidationLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Validation Level")
    )

    description = models.TextField (verbose_name=_("Description"),blank=True, null=True)

    created_at = jmodels.jDateField(auto_now_add=True)
    updated_at = jmodels.jDateField(auto_now=True)

    class Meta:

        verbose_name = _("Call Report")
        verbose_name_plural = _("Call Reports")
        ordering = ['-number']

    def __str__(self):
        return f"{self.number or 'No Number'} - {self.name or 'Unnamed'}"
    
####################################################################################
# All Model Cargo Announcement

class ProductType (models.Model):

    name = models.CharField(max_length=100, verbose_name=_("Product Type Name"))
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_("Parent Product Type")
    )

    class Meta:
        verbose_name = _("Product Type Level")
        verbose_name_plural = _("Product Type Levels")

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
# model PortName
class PortName (models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Port Name"))
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_("Parent Port Name")
    )

    class Meta:
        verbose_name = _("Port Name Level")
        verbose_name_plural = _("Port Name Levels")

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

# model CountryName
class CountryName (models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Country Name"))
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_("Parent Country Name")
    )

    class Meta:
        verbose_name = _("Country Name Level")
        verbose_name_plural = _("Country Name Levels")

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
class LoadingTime (models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Loading Time"))
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_("Parent Loading Time")
    )

    class Meta:
        verbose_name = _("Loading Time Level")
        verbose_name_plural = _("Loading Time Levels")

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    
# Original Model Cargo Announcement
class CargoAnnouncement (models.Model):

    class LoadType(models.TextChoices):
        PERSONAL = 'personal', _("Personal")
        COMPANY = 'company', _("Company")

    load_type = models.CharField(
        max_length=20,
        choices=LoadType.choices,
        default=LoadType.PERSONAL,
        verbose_name=_("Load Type")
    )

    full_name = models.CharField(max_length=100, verbose_name=_("full name"), blank=True, null=True)
    number = models.IntegerField(verbose_name=_("number"), blank=True, null=True)

    name_company = models.CharField (max_length=100, verbose_name=_("name company"), blank=True, null=True)
    name_ceo =  models.CharField (max_length=100, verbose_name=_("name ceo"), blank=True, null=True)
    number_ceo = models.CharField (max_length=100, verbose_name=_("number ceo"), blank=True, null=True)



    product_type = models.ForeignKey(
    ProductType,
    on_delete=models.PROTECT,  
    null=True,
    blank=True,
    verbose_name=_("Product Type"),
    related_name='CargoAnnouncement'
    )

    port_name = models.ForeignKey(
    PortName,
    on_delete=models.PROTECT,
    null=True,
    blank=True,
    verbose_name = _("Port Name"),
    related_name='CargoAnnouncement'
    )

    country_name = models.ForeignKey(
    CountryName,
    on_delete=models.PROTECT,
    null=True,
    blank=True,
    verbose_name = _("Country Name"),
    related_name='CargoAnnouncement'
    )

    loading_time = models.ForeignKey(
    LoadingTime,
    on_delete=models.PROTECT,
    null=True,
    blank=True,
    verbose_name = _("Loading Time"),
    related_name='CargoAnnouncement'
    )



    class Meta:
        verbose_name = _("CargoAnnouncement")
        verbose_name_plural = _("CargoAnnouncement")

    def __str__(self):
        if self.load_type == self.LoadType.COMPANY and self.name_company:
            return f"{self.name_company} ({self.name_ceo} → {self.number_ceo})"
        else:
            return f"{self.full_name} {self.number}"
