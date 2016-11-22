from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from . import models


class CategoryAdmin(admin.ModelAdmin):
	fields = ['name', 'description', 'image']
	list_display = ('name',)


class ProductInLine(admin.StackedInline):
    model = models.Product


class BundleAdmin(admin.ModelAdmin):
	fields = ['category', 'name', 'description', 'image', 'user']
	list_display = ('name',)
	inlines = [ProductInLine,]


class ProfileInLine(admin.StackedInline):
    model = models.UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInLine, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Bundle, BundleAdmin)
