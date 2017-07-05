from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.models import User as DefaultUser
from rest_framework import serializers
from . import models

class Product(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Product
        fields = ('url', 'name', 'description', 'image', 'price', 'bundle')


class UserBrief(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(source='profile.image')

    class Meta:
        model = models.User
        fields = ('url', 'username', 'image')


class Bundle(serializers.HyperlinkedModelSerializer):
    user = UserBrief()
    products = Product(many=True, read_only=True)

    class Meta:
        model = models.Bundle
        fields = ('url', 'name', 'description', 'image', 'user', 'products', 'category')


class BundleCreate(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Bundle
        fields = ('url', 'name', 'description', 'image', 'category')


class BundleTile(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Bundle
        fields = ('url', 'name', 'image')


class CategoryTile(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Category
        fields = ('url', 'name', 'image')


class Category(serializers.HyperlinkedModelSerializer):
    bundles = BundleTile(many=True, read_only=True)

    class Meta:
        model = models.Category
        fields = ('url', 'name', 'description', 'image', 'bundles')


class User(serializers.HyperlinkedModelSerializer):
    bundles = BundleTile(many=True, read_only=True)
    image = serializers.ImageField(source='profile.image')

    class Meta:
        model = DefaultUser
        fields = ('url', 'username', 'bundles', 'image')

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


class EditUser(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(source='profile.image')

    class Meta:
        model = DefaultUser
        fields = ('url', 'username', 'image')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super(EditUser, self).create(validated_data)
        self.create_or_update_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        self.create_or_update_profile(instance, profile_data)
        return super(EditUser, self).update(instance, validated_data)

    def create_or_update_profile(self, user, profile_data):
        profile, created = models.UserProfile.objects.get_or_create(user=user, defaults=profile_data)
        if not created and profile_data is not None:
            super(EditUser, self).update(profile, profile_data)