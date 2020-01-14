from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['id', 'category']


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = Category
        exclude = ['id']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertImage
        exclude = ['product']


class AdvertSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    category = CategorySerializer()
    product = ProductSerializer()
    #user = UserSerializer()
    class Meta:
        model = Advert
        exclude = ['phone', 'is_active', 'user', 'is_deleted']
