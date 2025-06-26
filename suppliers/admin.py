from django.contrib import admin

from .models import Contact, Product, Supplier


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "country", "city", "street", "house_number")
    search_fields = ("city", "street", "email")
    list_filter = ("country", "city")
    ordering = ("city",)
    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Адрес", {"fields": ("country", "city", "street", "house_number")}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date")
    search_fields = ("name", "model")
    list_filter = ("release_date",)
    ordering = ("-release_date",)
    fieldsets = (
        (None, {"fields": ("name", "model")}),
        ("Дата выхода", {"fields": ("release_date",)}),
    )


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contacts_city", "supplier_link", "debt", "level", "created_at")
    list_filter = ("contacts__city", "level")
    search_fields = ("name",)
    readonly_fields = ("created_at", "level")
    autocomplete_fields = ("supplier",)
    fieldsets = (
        (None, {"fields": ("name", "contacts", "products")}),
        ("Связь с поставщиком", {"fields": ("supplier",)}),
        ("Финансы и дата создания", {"fields": ("debt", "created_at", "level")}),
    )
    actions = ["clear_selected_suppliers_debt"]
    filter_horizontal = ("products",)

    def contacts_city(self, obj):
        return obj.contacts.city if obj.contacts else "-"

    contacts_city.short_description = "Город"

    def supplier_link(self, obj):
        if obj.supplier:
            return obj.supplier.name
        return "-"

    supplier_link.short_description = "Поставщик"

    def clear_selected_suppliers_debt(self, request, queryset):
        updated_count = queryset.update(debt=0.00)
        self.message_user(request, f"Обнулен долг у {updated_count} объектов")

    clear_selected_suppliers_debt.short_description = "Очистить задолженность у выбранных объектов"
