from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global
from easy_thumbnails.files import get_thumbnailer
from rest_framework.authtoken.models import Token


saved_file.connect(generate_aliases_global)

class Category(models.Model):
	name = models.CharField(max_length=255, unique=True)
	description = models.TextField()
	image = ThumbnailerImageField(resize_source=dict(size=(80, 80), sharpen=True))

	def __str__(self):
		return self.name


class Bundle(models.Model):
	category = models.ForeignKey(Category, related_name='bundles')
	name = models.CharField(max_length=255, unique=True)
	description = models.TextField()
	image = ThumbnailerImageField(resize_source=dict(size=(80, 80), sharpen=True),
		default=settings.MEDIA_ROOT+'/default.jpg')
	user = models.ForeignKey(User, related_name='bundles')

	def __str__(self):
		return self.name


class Product(models.Model):
	bundle = models.ForeignKey(Bundle, related_name='products')
	name = models.CharField(max_length=255)
	description = models.TextField()
	price = models.DecimalField(max_digits=12, decimal_places=3)
	image = ThumbnailerImageField(resize_source=dict(size=(80, 80), sharpen=True),
		default=settings.MEDIA_ROOT+'/default.jpg')

	def __str__(self):
		return self.name


@receiver(post_save, sender='auth.User')
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)