# products/serializers.py
import json
from rest_framework import serializers
from .models import Category, SubCategory, Brand, Product, ProductAttribute



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category', 'description', 'image']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'image']

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'value', 'additional_price']

class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True, required=False)
    rating = serializers.FloatField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    brand_id = serializers.IntegerField(source='brand.id', read_only=True)
    image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'subcategory', 'brand', 'brand_id', 'brand_name',
            'name', 'description', 'composition', 'price', 'stock', 'image',
            'attributes', 'rating', 'rating_count', 'subcategory_name'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)

        return None



    def create(self, validated_data):
        # Extract attributes data
        attributes_data = validated_data.pop('attributes', [])
        
        # Create the Product instance
        product = Product.objects.create(**validated_data)

        # Add attributes if provided
        if attributes_data:
            for attr in attributes_data:
                if isinstance(attr, str):  # Parse JSON string if necessary
                    attr = json.loads(attr)
                ProductAttribute.objects.create(product=product, **attr)

        return product

    def update(self, instance, validated_data):
        # Extract attributes data
        attributes_data = validated_data.pop('attributes', None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle attributes
        if attributes_data is not None:
            if isinstance(attributes_data, str):  # Parse JSON string if necessary
                try:
                    attributes_data = json.loads(attributes_data)
                except json.JSONDecodeError:
                    raise serializers.ValidationError("Invalid JSON format for attributes.")

            # Clear existing attributes and add new ones
            instance.attributes.all().delete()
            for attr in attributes_data:
                ProductAttribute.objects.create(product=instance, **attr)

        instance.save()
        return instance
