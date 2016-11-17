from django.contrib import admin
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


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Bundle, BundleAdmin)
