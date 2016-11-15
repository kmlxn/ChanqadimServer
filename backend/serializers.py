from django.contrib.auth.models import User
from .models import Category, Bundle
from rest_framework import serializers


class BundleSerializer(serializers.HyperlinkedModelSerializer):
    # category = serializers.HyperlinkedRelatedField(view_name='category-detail', read_only=True)

    class Meta:
        model = Bundle
        fields = ('url', 'category', 'name', 'description', 'image', 'user')


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
