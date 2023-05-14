from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ProveedorResource(resources.ModelResource):
    class Meta:
        model = Proveedor


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("auth_user_id", "company_name", "phone_number", "created_at")
    resource_class = ProveedorResource
    search_fields = ("auth_user_id", "company_name")
    #  list_filter= ("auth_user_id")


class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente


class ClienteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("dni", "nombres", "apellidos", "celular", "created_at")
    resource_class = ClienteResource
    search_fields = ("dni", "apellidos")
    #  list_filter= ("auth_user_id")


class ProductsResource(resources.ModelResource):
    class Meta:
        model = Products


class ProductsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "categories_id",
        "product_name",
        "price",
        "product_description",
        "created_at",
    )
    resource_class = ProductsResource
    search_fields = ("id", "categories_id", "product_name")
    #  list_filter= ("auth_user_id")


class StockResource(resources.ModelResource):
    class Meta:
        model = Stock


class StockAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "products",
        "cantidad_stock",
        "descripcion",
        "precio",
    )
    resource_class = ProductsResource
    search_fields = ("id", "products")
    #  list_filter= ("auth_user_id")


admin.site.register(CustomUser)
admin.site.register(AdminUser)
admin.site.register(StaffUser)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Categorie)
admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductMedia)
admin.site.register(OrderStock)
admin.site.register(Stock, StockAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payments)
admin.site.register(OrderDeliveryStatus)
