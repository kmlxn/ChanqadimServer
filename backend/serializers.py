from django.contrib.auth.models import User
from .models import Category, Bundle, Product
from rest_framework import serializers


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('url', 'name', 'description', 'image', 'price')


class BundleSerializer(serializers.HyperlinkedModelSerializer):
    # category = serializers.HyperlinkedRelatedField(view_name='category-detail', read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Bundle
        fields = ('url', 'category', 'name', 'description', 'image', 'user', 'products')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    bundles = BundleSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('url', 'name', 'description', 'image', 'bundles')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    bundles = BundleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'bundles')
