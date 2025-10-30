from rest_framework import serializers
from app.crm.models import FieldActivity, ValidationLevel, CallReport, CargoAnnouncement, ProductType, PortName, CountryName, LoadingTime, TransactionType, PurchaseProcess, SaleReport, MarketPlace, MarketOutside, Quota, Overhead, SupplyStatus
from rest_framework.reverse import reverse

# ─────────────────────────────
# FieldActivity Serializer
# ─────────────────────────────
class FieldActivitySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = FieldActivity
        fields = ['id', 'name', 'parent', 'parent_name']


# ─────────────────────────────
# ValidationLevel Serializer
# ─────────────────────────────
class ValidationLevelSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = ValidationLevel
        fields = ['id', 'name', 'parent', 'parent_name']


# ─────────────────────────────
# CallReport Serializer
# ─────────────────────────────
class CallReportSerializer(serializers.ModelSerializer):
    field_activity = FieldActivitySerializer(read_only=True)
    validation = ValidationLevelSerializer(read_only=True)
    purchase_process_url = serializers.SerializerMethodField(read_only=True)
    absolute_url = serializers.SerializerMethodField(read_only=True)

   
    field_activity_id = serializers.PrimaryKeyRelatedField(
        source='field_activity', queryset=FieldActivity.objects.all(), write_only=True, required=False
    )
    validation_id = serializers.PrimaryKeyRelatedField(
        source='validation', queryset=ValidationLevel.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = CallReport
        fields = [
            'id', 'number', 'name', 'province', 'city',
            'field_activity', 'field_activity_id',
            'last_purchase', 'purchase_satisfaction',
            'validation', 'validation_id',
            'description', 'created_at', 'updated_at','absolute_url','purchase_process_url',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_absolute_url(self, obj):
        # Generate absolute URL for the post
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def get_purchase_process_url(self, obj):
        request = self.context.get('request')
        if not request:
            return None

        purchase_process = getattr(obj, 'purchase_process', None)
        if not purchase_process:
            return request.build_absolute_uri(f'/crm/api/v1/call-reports/{obj.id}/go-to-purchase/')
        return request.build_absolute_uri(f'/crm/api/v1/purchase-process/{purchase_process.id}/')
    
    def to_representation(self, instance):
       
        rep = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.parser_context:
            view_kwargs = request.parser_context.get('kwargs', {})
            if view_kwargs.get('pk'):
                
                rep.pop('absolute_url', None)

        return rep

########################################################################


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ProductTypeSerializer(serializers.ModelSerializer):
    parent = serializers.CharField(source='parent.name', read_only=True)
    children = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = ProductType
        fields = ['id', 'name', 'parent', 'children']


class PortNameSerializer(serializers.ModelSerializer):
    parent = serializers.CharField(source='parent.name', read_only=True)
    children = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = PortName
        fields = ['id', 'name', 'parent', 'children']


class CountryNameSerializer(serializers.ModelSerializer):
    parent = serializers.CharField(source='parent.name', read_only=True)
    children = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = CountryName
        fields = ['id', 'name', 'parent', 'children']


class LoadingTimeSerializer(serializers.ModelSerializer):
    parent = serializers.CharField(source='parent.name', read_only=True)
    children = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = LoadingTime
        fields = ['id', 'name', 'parent', 'children']


class TransactionTypeSerializer(serializers.ModelSerializer):
    parent = serializers.CharField(source='parent.name', read_only=True)
    children = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = TransactionType
        fields = ['id', 'name', 'parent', 'children']


class CargoAnnouncementSerializer(serializers.ModelSerializer):
    
    product_type_id = serializers.PrimaryKeyRelatedField(
        source='product_type', queryset=ProductType.objects.all(), write_only=True, required=False, allow_null=True
    )
    port_name_id = serializers.PrimaryKeyRelatedField(
        source='port_name', queryset=PortName.objects.all(), write_only=True, required=False, allow_null=True
    )
    country_name_id = serializers.PrimaryKeyRelatedField(
        source='country_name', queryset=CountryName.objects.all(), write_only=True, required=False, allow_null=True
    )
    loading_time_id = serializers.PrimaryKeyRelatedField(
        source='loading_time', queryset=LoadingTime.objects.all(), write_only=True, required=False, allow_null=True
    )
    transaction_type_id = serializers.PrimaryKeyRelatedField(
        source='transaction_type', queryset=TransactionType.objects.all(), write_only=True, required=False, allow_null=True
    )

   
    product_type = ProductTypeSerializer(read_only=True)
    port_name = PortNameSerializer(read_only=True)
    country_name = CountryNameSerializer(read_only=True)
    loading_time = LoadingTimeSerializer(read_only=True)
    transaction_type = TransactionTypeSerializer(read_only=True)

    number = serializers.IntegerField(required=False, allow_null=True)
    absolute_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CargoAnnouncement
        fields = [
            'id', 'load_type', 'full_name', 'number', 'name_company', 'name_ceo', 'number_ceo', 'sales_expert_name',
            'product_price', 'description',
            # write-only
            'product_type_id', 'port_name_id', 'country_name_id', 'loading_time_id', 'transaction_type_id',
            # read-only nested
            'product_type', 'port_name', 'country_name', 'loading_time', 'transaction_type',
            'absolute_url',
        ]
    def get_absolute_url(self, obj):
        # Generate absolute URL for the post
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        if request and "go-to-purchase" in request.path:
            rep["absolute_url"] = request.build_absolute_uri(
                f"/crm/api/v1/cargo-announcements/{instance.id}/"
            )

        if request and request.parser_context.get("kwargs", {}).get("pk"):
            rep.pop("absolute_url", None)

        return rep
    
#######################################################################

class PurchaseProcessSerializer(serializers.ModelSerializer):
    call_report_name = serializers.CharField(source='call_report.name', read_only=True)
    call_report_number = serializers.CharField(source='call_report.number', read_only=True)
    sale_report = serializers.SerializerMethodField(read_only=True)
    absolute_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PurchaseProcess
        fields = [
            'id', 'load_type', 'call_report', 'call_report_name', 'call_report_number',
            'market_place_type', 'yekta_code', 'market_outside_address', 'postal_code',
            'market_outside_number', 'buyer_name', 'overhead_address', 'overhead_number',
            'agreement_kotazh', 'cash_user', 'cash_password', 'cash_kotazh',
            'destination_name', 'quota_number', 'created_at', 'absolute_url','sale_report',
        ]

        extra_kwargs = {
            'call_report': {'write_only': True}
        }

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    def get_sale_report(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        sale_report = getattr(obj, 'sale_report', None)
        if sale_report:
            return request.build_absolute_uri(f'/crm/api/v1/sale-reports/{sale_report.id}/')
        else:
            return request.build_absolute_uri(f'/crm/api/v1/purchase-process/{obj.id}/go-to-sale-report/')
        
    def to_representation(self, instance):
        
        rep = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.method == 'GET':
            allowed_fields = ['id', 'load_type', 'call_report_name', 'call_report_number', 'sale_report', 'absolute_url', 'created_at']
            if instance.load_type == 'market_place':
                allowed_fields.append('market_place_type')
                m_type = getattr(instance, 'market_place_type', None)
                if m_type == 'agreement':
                    allowed_fields.append('agreement_kotazh')
                elif m_type == 'cash':
                    allowed_fields += ['cash_user', 'cash_password', 'cash_kotazh']
            elif instance.load_type == 'market_outside':
                allowed_fields += ['yekta_code', 'market_outside_address', 'postal_code', 'market_outside_number', 'buyer_name']
            elif instance.load_type == 'quota':
                allowed_fields += ['destination_name', 'quota_number']
            elif instance.load_type == 'overhead':
                allowed_fields += ['overhead_address', 'overhead_number']

            rep = {k: v for k, v in rep.items() if k in allowed_fields}

       
        if request and "go-to-purchase" in request.path:
            rep["absolute_url"] = request.build_absolute_uri(
                f"/crm/api/v1/purchase-process/{instance.id}/"
            )

        if request and request.parser_context.get("kwargs", {}).get("pk"):
            rep.pop("call_report", None)
            rep.pop("absolute_url", None)

        return rep
    
    
########################################################################

# --- SupplyStatus ---
class SupplyStatusSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    parent = serializers.PrimaryKeyRelatedField(
        queryset=SupplyStatus.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = SupplyStatus
        fields = ['id', 'name', 'parent', 'parent_name']


# --- MarketPlace ---
class MarketPlaceSerializer(serializers.ModelSerializer):
    sale_report = serializers.PrimaryKeyRelatedField(read_only=True)
    supply_status_name = serializers.SerializerMethodField(read_only=True)
    supply_status = serializers.PrimaryKeyRelatedField(
        queryset=SupplyStatus.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = MarketPlace
        fields = [
            'id',
            'sale_report',
            'product_name',
            'weight',
            'market_price',
            'purchase_price',
            'selling_price',
            'profit',
            'unofficial',
            'total_amount',
            'deposit',
            'account_remaining',
            'buyer',
            'seller',
            'supplier',
            'supply_status',
            'supply_status_name',
            'sales_expert_name',
            'description',
            'weight_barname',
        ]

    def get_supply_status_name(self, obj):
        return obj.supply_status.name if obj.supply_status else None
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in ['profit', 'unofficial', 'total_amount', 'account_remaining']:
            if rep.get(field) is not None:
                rep[field] = int(float(rep[field]))   
        return rep


# --- MarketOutside ---
class MarketOutsideSerializer(serializers.ModelSerializer):
    sale_report = serializers.PrimaryKeyRelatedField(read_only=True)

    supply_status_name = serializers.SerializerMethodField(read_only=True)
    supply_status = serializers.PrimaryKeyRelatedField(
        queryset=SupplyStatus.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = MarketOutside
        fields = [
            'id',
            'sale_report',
            'product_name',
            'weight',
            'purchase_price',
            'selling_price',
            'profit',
            'total_amount',
            'deposit',
            'account_remaining',
            'buyer',
            'seller',
            'supplier',
            'supply_status_name',
            'supply_status',
            'sales_expert_name',
            'description',
            'weight_barname',
        ]
    def get_supply_status_name(self, obj):
        return obj.supply_status.name if obj.supply_status else None
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in ['profit', 'total_amount', 'account_remaining']:
            if rep.get(field) is not None:
                rep[field] = int(float(rep[field]))   
        return rep


# --- Quota ---
class QuotaSerializer(serializers.ModelSerializer):
    sale_report = serializers.PrimaryKeyRelatedField(read_only=True)

    supply_status_name = serializers.SerializerMethodField(read_only=True)
    supply_status = serializers.PrimaryKeyRelatedField(
        queryset=SupplyStatus.objects.all(),
        required=False,
        allow_null=True
    )
    class Meta:
        model = Quota
        fields = [
            'id',
            'sale_report',
            'product_name',
            'weight',
            'purchase_price',
            'selling_price',
            'profit',
            'total_amount',
            'deposit',
            'account_remaining',
            'buyer',
            'seller',
            'supplier',
            'supply_status',
            'supply_status_name',
            'sales_expert_name',
            'description',
        ]

    def get_supply_status_name(self, obj):
        return obj.supply_status.name if obj.supply_status else None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in ['profit', 'total_amount', 'account_remaining']:
            if rep.get(field) is not None:
                rep[field] = int(float(rep[field]))   
        return rep


# --- Overhead ---
class OverheadSerializer(serializers.ModelSerializer):
    sale_report = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Overhead
        fields = [
            'id',
            'sale_report',
            'address',
            'number'
        ]


# --- SaleReport  ---
class SaleReportSerializer(serializers.ModelSerializer):
    marketplace = MarketPlaceSerializer(required=False)
    marketoutside = MarketOutsideSerializer(required=False)
    quota = QuotaSerializer(required=False)
    overhead = OverheadSerializer(required=False)
    absolute_url = serializers.SerializerMethodField(read_only=True)
    export = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SaleReport
        fields = [
            'id',
            'purchase_process',
            'sale_type',
            'sale_date',
            'marketplace',
            'marketoutside',
            'quota',
            'overhead',
            'absolute_url',
            'export',
        ]

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def get_export(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse('sale-report-export', kwargs={'pk': obj.pk})  
            )
        return None
    
    def create(self, validated_data):
        marketplace_data = validated_data.pop('marketplace', None)
        marketoutside_data = validated_data.pop('marketoutside', None)
        quota_data = validated_data.pop('quota', None)
        overhead_data = validated_data.pop('overhead', None)

        sale_report = SaleReport.objects.create(**validated_data)

        if marketplace_data:
            MarketPlace.objects.create(sale_report=sale_report, **marketplace_data)
        if marketoutside_data:
            MarketOutside.objects.create(sale_report=sale_report, **marketoutside_data)
        if quota_data:
            Quota.objects.create(sale_report=sale_report, **quota_data)
        if overhead_data:
            Overhead.objects.create(sale_report=sale_report, **overhead_data)

        return sale_report

    def update(self, instance, validated_data):
        marketplace_data = validated_data.pop('marketplace', None)
        marketoutside_data = validated_data.pop('marketoutside', None)
        quota_data = validated_data.pop('quota', None)
        overhead_data = validated_data.pop('overhead', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        def update_or_create(related_instance, model_class, data):
            if related_instance:
                for attr, value in data.items():
                    setattr(related_instance, attr, value)
                related_instance.save()
            else:
                model_class.objects.create(sale_report=instance, **data)

        if marketplace_data:
            update_or_create(getattr(instance, 'marketplace', None), MarketPlace, marketplace_data)
        if marketoutside_data:
            update_or_create(getattr(instance, 'marketoutside', None), MarketOutside, marketoutside_data)
        if quota_data:
            update_or_create(getattr(instance, 'quota', None), Quota, quota_data)
        if overhead_data:
            update_or_create(getattr(instance, 'overhead', None), Overhead, overhead_data)

        return instance
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        view = self.context.get('view')

    # ---  absolute_url ---
        if view:
            pk = view.kwargs.get('pk')
            if pk:
                rep.pop('absolute_url', None)

    # --- sale_type ---
        sale_type = instance.sale_type  
        if sale_type == "market_place":
            rep.pop("marketoutside", None)
            rep.pop("quota", None)
            rep.pop("overhead", None)
        elif sale_type == "market_outside":
            rep.pop("marketplace", None)
            rep.pop("quota", None)
            rep.pop("overhead", None)
        elif sale_type == "quota":
            rep.pop("marketplace", None)
            rep.pop("marketoutside", None)
            rep.pop("overhead", None)
        elif sale_type == "overhead":
            rep.pop("marketplace", None)
            rep.pop("marketoutside", None)
            rep.pop("quota", None)

        return rep
    
class SaleReportExportSerializer(serializers.ModelSerializer):
    sale_type_display = serializers.CharField(source='get_sale_type_display', read_only=True)
    supply_status_name = serializers.CharField(source='marketplace.supply_status_name', read_only=True)
    sales_expert_name = serializers.CharField(source='marketplace.sales_expert_name', read_only=True)
    
    class Meta:
        model = SaleReport
        fields = [
            "sale_date",
            "sale_type_display",
            "profit",
            "total_amount",
            "account_remaining",
            "supply_status_name",
            "sales_expert_name",
            "description",
        ]