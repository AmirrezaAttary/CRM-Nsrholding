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
################################################################################

class PurchaseProcess(models.Model):

    class LoadType(models.TextChoices):
        MARKET_PLACE = 'market_place', _("MarketPlace")
        MARKET_OUTSIDE = 'market_outside', _("MarketOutside")
        QUOTA = 'quota', _("Quota")
        OVERHEAD = 'overhead', _("Overhead")

    class MarketPlaceType(models.TextChoices):
        AGREEMENT = 'agreement', _("Agreement")
        CASH = 'cash', _("Cash")

    load_type = models.CharField(
        max_length=20,
        choices=LoadType.choices,
        default=LoadType.MARKET_PLACE,
        verbose_name=_("Purchase type")
    )

    call_report = models.OneToOneField(
        'CallReport',
        on_delete=models.CASCADE,
        related_name='purchase_process',
        verbose_name=_("Call Report")
    )

    market_place_type = models.CharField(
        max_length=20,
        choices=MarketPlaceType.choices,
        blank=True,
        null=True,
        verbose_name=_("MarketPlace Type")
    )

    # --------------------------
    # MARKET OUTSIDE Fields
    # --------------------------
    yekta_code = models.CharField(max_length=100, verbose_name=_("Yekta Code"), blank=True, null=True)
    market_outside_address = models.CharField(max_length=255, verbose_name=_("Market Outside Address"), blank=True, null=True)
    postal_code = models.CharField(max_length=20, verbose_name=_("Postal Code"), blank=True, null=True)
    market_outside_number = models.CharField(max_length=50, verbose_name=_("Market Outside Number"), blank=True, null=True)
    buyer_name = models.CharField(max_length=100, verbose_name=_("Buyer Name"), blank=True, null=True)

    # --------------------------
    # OVERHEAD Fields
    # --------------------------
    overhead_address = models.CharField(max_length=255, verbose_name=_("Overhead Address"), blank=True, null=True)
    overhead_number = models.CharField(max_length=50, verbose_name=_("Overhead Number"), blank=True, null=True)

    # --------------------------
    # MARKET PLACE Fields
    # --------------------------
    agreement_kotazh = models.CharField(max_length=100, verbose_name=_("Agreement Kotazh"), blank=True, null=True)
    
    cash_user = models.CharField(max_length=100, verbose_name=_("Cash User"), blank=True, null=True)
    cash_password = models.CharField(max_length=100, verbose_name=_("Cash Password"), blank=True, null=True)
    cash_kotazh = models.CharField(max_length=100, verbose_name=_("Cash Kotazh"), blank=True, null=True)

    # --------------------------
    # QUOTA Fields
    # --------------------------
    destination_name = models.CharField(max_length=150, verbose_name=_("Destination Name"), blank=True, null=True)
    quota_number = models.CharField(max_length=50, verbose_name=_("Quota Number"), blank=True, null=True)

    # --------------------------
    # SYSTEM Fields
    # --------------------------
    created_at = jmodels.jDateField(auto_now_add=True, verbose_name=_("Created At"),blank=True,null=True)
    updated_at = jmodels.jDateField(auto_now=True, verbose_name=_("Updated At"),blank=True,null=True)

    class Meta:
        verbose_name = _("Purchase Process")
        verbose_name_plural = _("Purchase Processes")
        ordering = ["-created_at"]

    def __str__(self):
        base_name = getattr(self.call_report, "name", None) or "Unknown"
        if self.load_type == self.LoadType.MARKET_PLACE:
            return f"{base_name} - MarketPlace ({self.market_place_type or 'Unknown'})"
        elif self.load_type == self.LoadType.MARKET_OUTSIDE:
            return f"{base_name} - {self.buyer_name or 'Outside Buyer'}"
        elif self.load_type == self.LoadType.QUOTA:
            return f"{base_name} - Quota ({self.destination_name or 'Unknown'})"
        elif self.load_type == self.LoadType.OVERHEAD:
            return f"{base_name} - Overhead"
        return base_name

###################################################################################
# ─────────────────────────────
#  MAIN MODEL
# ─────────────────────────────
class SaleReport(models.Model):
    class SaleType(models.TextChoices):
        MARKET_PLACE = 'market_place', _("MarketPlace")
        MARKET_OUTSIDE = 'market_outside', _("MarketOutside")
        QUOTA = 'quota', _("Quota")
        OVERHEAD = 'overhead', _("Overhead")

    purchase_process = models.OneToOneField(
        PurchaseProcess,
        on_delete=models.CASCADE,
        related_name='sale_report',
        verbose_name=_("Purchase Process")
    )

    sale_type = models.CharField(
        max_length=20,
        choices=SaleType.choices,
        verbose_name=_("Sale Type")
    )

    sale_date = jmodels.jDateField(verbose_name=_("Sale Date"), blank=True, null=True)

    class Meta:
        verbose_name = _("Sale Report")
        verbose_name_plural = _("Sale Reports")
        ordering = ['-sale_date']

    def __str__(self):
        return f"{self.purchase_process.call_report.name if hasattr(self.purchase_process, 'call_report') else 'Unknown'} - {self.get_sale_type_display()}"
    
# ForeignKey SupplyStatus
class SupplyStatus (models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Supply Status"))
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_("Parent Supply Status")
    )

    class Meta:
        verbose_name = _("Supply Status Level")
        verbose_name_plural = _("Supply Status Levels")
        ordering = ['name']

    def __str__(self):
        return f"{self.parent.name} > {self.name}" if self.parent else self.name
    
# ForeignKey MarketPlace
class MarketPlace(models.Model):
    sale_report = models.OneToOneField(
        SaleReport,
        on_delete=models.CASCADE,
        related_name='marketplace',
        verbose_name=_("Sale Report")
    )

    product_name = models.CharField(max_length=100, verbose_name=_("Product Name"), blank=True, null=True)
    weight = models.IntegerField(verbose_name=_("Weight"), blank=True, null=True)
    market_price = models.IntegerField(verbose_name=_("Market Price"), blank=True, null=True)
    purchase_price = models.IntegerField(verbose_name=_("Purchase Price"), blank=True, null=True)
    selling_price = models.IntegerField(verbose_name=_("Selling Price"), blank=True, null=True)
    profit = models.DecimalField(max_digits=15, decimal_places=2,verbose_name=_("Profit"), null=False, blank=False, default=0)
    unofficial = models.DecimalField(max_digits=15, decimal_places=2,verbose_name=_("Unofficial"), null=False, blank=False, default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2,verbose_name=_("Total Amount"), null=False, blank=False, default=0)
    deposit = models.IntegerField(verbose_name=_("Deposit"), blank=True, null=True)
    account_remaining = models.DecimalField(max_digits=15, decimal_places=2,verbose_name=_("Account Remaining"), null=False, blank=False, default=0)
    
    buyer = models.BooleanField(default=False, verbose_name=_("Buyer"))
    seller = models.BooleanField(default=False, verbose_name=_("Seller"))
    supplier = models.BooleanField(default=False, verbose_name=_("Supplier"))

    supply_status = models.ForeignKey(
        SupplyStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("MarketPlace Supply Status Level")
    )

    sales_expert_name = models.CharField(max_length=100, verbose_name=_("Sales Expert Name"), blank=True, null=True)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    weight_barname = models.IntegerField(verbose_name=_("Weight Barname"), blank=True, null=True)

    class Meta:
        verbose_name = _("MarketPlace Sale")
        verbose_name_plural = _("MarketPlace Sales")
        ordering = ['-id']

    def __str__(self):
        return f"{self.product_name or 'Unnamed Product'} ({self.selling_price or 0} Rls)"
    
    def save(self, *args, **kwargs):
        # total_amount = weight * selling_price
        if self.weight is not None and self.selling_price is not None:
            self.total_amount = self.weight * self.selling_price
        else:
            self.total_amount = 0

        # profit = selling_price - purchase_price * weight
        if self.selling_price is not None and self.purchase_price is not None and self.weight is not None:
            self.profit = (self.selling_price - self.purchase_price) * self.weight
        else:
            self.profit = 0

        # unofficial = selling_price - market_price * weight
        if self.selling_price is not None and self.market_price is not None and self.weight is not None:
            self.unofficial = (self.selling_price - self.market_price) * self.weight
        else:
            self.unofficial = 0

        # account_remaining = deposit - total_amount
        if self.deposit is not None:
            self.account_remaining = self.deposit - self.total_amount
        else:
            self.account_remaining = -self.total_amount

        super().save(*args, **kwargs)



class MarketOutside(models.Model):
    sale_report = models.OneToOneField(
        SaleReport,
        on_delete=models.CASCADE,
        related_name='marketoutside',
        verbose_name=_("Sale Report")
    )

    product_name = models.CharField(max_length=100, verbose_name=_("Product Name"), blank=True, null=True)
    weight = models.IntegerField(verbose_name=_("Weight"), blank=True, null=True)
    purchase_price = models.IntegerField(verbose_name=_("Purchase Price"), blank=True, null=True)
    selling_price = models.IntegerField(verbose_name=_("Selling Price"), blank=True, null=True)
    profit = models.DecimalField(max_digits=15, decimal_places=2,verbose_name=_("Profit"), blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2,verbose_name=_("Total Amount"), null=False, blank=False, default=0)
    deposit = models.IntegerField(verbose_name=_("Deposit"), blank=True, null=True)
    account_remaining = models.DecimalField(max_digits=15, decimal_places=2,verbose_name=_("Account Remaining"), null=False, blank=False, default=0)
    
    buyer = models.BooleanField(default=False, verbose_name=_("Buyer"))
    seller = models.BooleanField(default=False, verbose_name=_("Seller"))
    supplier = models.BooleanField(default=False, verbose_name=_("Supplier"))

    supply_status = models.ForeignKey(
        SupplyStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("MarketOutside Supply Status Level")
    )

    sales_expert_name = models.CharField(max_length=100, verbose_name=_("Sales Expert Name"), blank=True, null=True)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    weight_barname = models.IntegerField(verbose_name=_("Weight Barname"), blank=True, null=True)

    class Meta:
        verbose_name = _("Market Outside Sale")
        verbose_name_plural = _("Market Outside Sales")
        ordering = ['-id']

    def __str__(self):
        return f"{self.product_name or 'Unnamed Product'} ({self.selling_price or 0} Rls)"
    
    def save(self, *args, **kwargs):
        # total_amount = weight * selling_price
        if self.weight is not None and self.selling_price is not None:
            self.total_amount = self.weight * self.selling_price
        else:
            self.total_amount = 0

        # profit = selling_price - purchase_price * weight
        if self.selling_price is not None and self.purchase_price is not None and self.weight is not None:
            self.profit = (self.selling_price - self.purchase_price) * self.weight
        else:
            self.profit = 0

        # account_remaining = deposit - total_amount
        if self.deposit is not None:
            self.account_remaining = self.deposit - self.total_amount
        else:
            self.account_remaining = -self.total_amount

        super().save(*args, **kwargs)

class Quota(models.Model):
    sale_report = models.OneToOneField(
        SaleReport,
        on_delete=models.CASCADE,
        related_name='quota',
        verbose_name=_("Sale Report")
    )

    product_name = models.CharField(max_length=100, verbose_name=_("Product Name"), blank=True, null=True)
    weight = models.IntegerField(verbose_name=_("Weight"), blank=True, null=True)
    purchase_price = models.IntegerField(verbose_name=_("Purchase Price"), blank=True, null=True)
    selling_price = models.IntegerField(verbose_name=_("Selling Price"), blank=True, null=True)
    profit = models.DecimalField(max_digits=15, decimal_places=2,verbose_name=_("Profit"), null=False, blank=False, default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2,verbose_name=_("Total Amount"), null=False, blank=False, default=0)
    deposit = models.IntegerField(verbose_name=_("Deposit"), blank=True, null=True)
    account_remaining = models.DecimalField(max_digits=15, decimal_places=2,verbose_name=_("Account Remaining"), null=False, blank=False, default=0)
    
    buyer = models.BooleanField(default=False, verbose_name=_("Buyer"))
    seller = models.BooleanField(default=False, verbose_name=_("Seller"))
    supplier = models.BooleanField(default=False, verbose_name=_("Supplier"))

    supply_status = models.ForeignKey(
        SupplyStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Quota Supply Status Level")
    )

    sales_expert_name = models.CharField(max_length=100, verbose_name=_("Sales Expert Name"), blank=True, null=True)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)

    class Meta:
        verbose_name = _("Quota Sale")
        verbose_name_plural = _("Quota Sales")
        ordering = ['-id']

    def __str__(self):
        return f"{self.product_name or 'Unnamed Product'} ({self.selling_price or 0} Rls)"
    
    def save(self, *args, **kwargs):
        # total_amount = weight * selling_price
        if self.weight is not None and self.selling_price is not None:
            self.total_amount = self.weight * self.selling_price
        else:
            self.total_amount = 0

        # profit = selling_price - purchase_price * weight
        if self.selling_price is not None and self.purchase_price is not None and self.weight is not None:
            self.profit = (self.selling_price - self.purchase_price) * self.weight
        else:
            self.profit = 0

        # account_remaining = deposit - total_amount
        if self.deposit is not None:
            self.account_remaining = self.deposit - self.total_amount
        else:
            self.account_remaining = -self.total_amount

        super().save(*args, **kwargs)

class Overhead(models.Model):
    sale_report = models.OneToOneField(
        SaleReport,
        on_delete=models.CASCADE,
        related_name='overhead',
        verbose_name=_("Sale Report")
    )

    address = models.CharField(max_length=100, verbose_name=_("Address"), blank=True, null=True)
    number = models.IntegerField(verbose_name=_("Number"), blank=True, null=True)

    class Meta:
        verbose_name = _("Overhead Sale")
        verbose_name_plural = _("Overhead Sales")
        ordering = ['-id']

    def __str__(self):
        return f"{self.address or 'Unknown Address'} ({self.number or 'No Number'})"
    

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
    
class TransactionType (models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Transaction Type"))
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_("Transaction Type")
    )

    class Meta:
        verbose_name = _("Transaction Type Level")
        verbose_name_plural = _("Transaction Type Levels")

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
    number = models.IntegerField(verbose_name=_("number"), blank=True, null=True,default=None)


    name_company = models.CharField (max_length=100, verbose_name=_("name company"), blank=True, null=True)
    name_ceo =  models.CharField (max_length=100, verbose_name=_("name ceo"), blank=True, null=True)
    number_ceo = models.CharField (max_length=100, verbose_name=_("number ceo"), blank=True, null=True)


    sales_expert_name = models.CharField (max_length=100, verbose_name=_("sales expert name"), blank=True, null=True)

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

    transaction_type = models.ForeignKey(
    TransactionType,
    on_delete=models.PROTECT,
    null=True,
    blank=True,
    verbose_name = _("Transaction Type"),
    related_name='CargoAnnouncement'
    )

    product_price = models.IntegerField(verbose_name=_("product price"), blank=True, null=True)

    description = models.TextField(verbose_name=_("description"), blank=True, null=True)


    class Meta:
        verbose_name = _("CargoAnnouncement")
        verbose_name_plural = _("CargoAnnouncement")

    def __str__(self):
        if self.load_type == self.LoadType.COMPANY and self.name_company:
            return f"{self.name_company} {self.name_ceo} {self.number_ceo}"
        else:
            return f"{self.full_name} {self.number}"
