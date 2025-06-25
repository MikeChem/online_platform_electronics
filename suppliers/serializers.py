from rest_framework import serializers
from .models import Supplier, Contact, Product

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'country', 'city', 'street', 'house_number']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'model', 'release_date']

class SupplierSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'contacts', 'products', 'supplier',
            'debt', 'created_at', 'level'
        ]
        read_only_fields = ['debt', 'created_at', 'level']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].method in ['GET']:
            data['supplier'] = instance.supplier.id if instance.supplier else None
        return data