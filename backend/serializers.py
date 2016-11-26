from django.contrib.auth.models import User
from .models import Category, Bundle, Product, UserProfile
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


class BundleTileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bundle
        fields = ('url', 'name', 'image')


class CategoryTileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'name', 'image')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    bundles = BundleTileSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('url', 'name', 'description', 'image', 'bundles')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    bundles = BundleSerializer(many=True, read_only=True)
    image = serializers.ImageField(source='profile.image')

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'bundles', 'image')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super(UserSerializer, self).create(validated_data)
        self.create_or_update_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        self.create_or_update_profile(instance, profile_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def create_or_update_profile(self, user, profile_data):
        profile, created = Profile.objects.get_or_create(user=user, defaults=profile_data)
        if not created and profile_data is not None:
            super(UserSerializer, self).update(profile, profile_data)