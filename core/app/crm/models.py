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
    
    
