from rest_framework import serializers
from .models import (
    CustomUser,
    AdminUser,
    StaffUser,
    Proveedor,
    Categorie,
    Products,
    ProductMedia,
    Stock,
    OrderStock,
)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "first_name", "last_name", "user_type")


class AdminUserSerializer(serializers.ModelSerializer):
    auth_user_id = CustomUserSerializer(read_only=True)

    class Meta:
        model = AdminUser
        fields = ("id", "profile_pic", "auth_user_id", "created_at")


class StaffUserSerializer(serializers.ModelSerializer):
    auth_user_id = CustomUserSerializer(read_only=True)

    class Meta:
        model = StaffUser
        fields = ("id", "profile_pic", "auth_user_id", "created_at")


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = "__all__"


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = "__all__"


class ProductsSerializer(serializers.ModelSerializer):
    categories_id = CategorieSerializer(read_only=True)

    class Meta:
        model = Products
        fields = "__all__"


class ProductMediaSerializer(serializers.ModelSerializer):
    product_id = ProductsSerializer(read_only=True)

    class Meta:
        model = ProductMedia
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = "__all__"


class OrderStockSerializer(serializers.ModelSerializer):
    Proveedor_id = ProveedorSerializer(read_only=True)
    product_id = ProductsSerializer(read_only=True)

    class Meta:
        model = OrderStock
        fields = "__all__"
