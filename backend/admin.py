from django.contrib import admin
from . import models

class CategoryAdmin(admin.ModelAdmin):
	fields = ['name', 'description', 'image']
	list_display = ('name',)

class BundleAdmin(admin.ModelAdmin):
	fields = ['category', 'name', 'description', 'image']
	list_display = ('name',)

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Bundle, BundleAdmin)
