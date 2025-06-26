from rest_framework import serializers

from .models import Contact, Product, Supplier


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "email", "country", "city", "street", "house_number"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "model", "release_date"]


class SupplierSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer()
    products = ProductSerializer(many=True, read_only=True)
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Supplier
        fields = ["id", "name", "contacts", "products", "supplier", "debt", "created_at", "level"]
        read_only_fields = ["debt", "created_at", "level"]

    def create(self, validated_data):
        contact_data = validated_data.pop("contacts")
        contact, _ = Contact.objects.get_or_create(**contact_data)

        return Supplier.objects.create(contacts=contact, **validated_data)
