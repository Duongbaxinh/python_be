from .import models
from rest_framework import serializers

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        # sử dụng __all__ để serializer tất cả các field được khai báo trong model
        fields = '__all__'

class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductComment
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    comments = ProductCommentSerializer(many=True, read_only=True)
    class Meta:
        model = models.Product
        # Khai báo từng field cụ thể, thêm custom field images và comments
        fields = (
        'id',
        'product_name',
        'product_rate',
        'product_price',
        'product_made',
        'discount',
        'amount',
        'is_public',
        'product_thumbnail',
        'product_brand',
        'product_genuine',
        'product_best',
        'product_des',
        'images',
        'comments',
        'category_id',
        'created_at',
        'updated_at',
        'deleted_at'
        )

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = models.Category
        fields = (
        'id',
        'name',
        'slug',
        'icon_url',
        'products',
        'created_at',
        'updated_at',
        'deleted_at'
        )

class InventorySerializer(serializers.ModelSerializer):
    # inventoryes = ProductImageSerializer(many = True)
    class Meta:
        model = models.Inventory
        fields = (
            'id',
            'inven_product',
            'inven_amount'
        )


class CartSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer()
    class Meta:
        model = models.Cart
        fields ="__all__"