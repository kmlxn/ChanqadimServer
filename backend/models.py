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

	def get_data(self):
		thumbnailer = get_thumbnailer(self.image)
		thumbnail_options = {'crop': True, 'size': (80, 80)}
		return {
			'key': self.pk,
			'name': self.name,
			'description': self.description,
			'image': thumbnailer.get_thumbnail(thumbnail_options).url,
			'bundles': [bundle.get_data() for bundle in self.bundle_set.all()],
		}


class Bundle(models.Model):
	category = models.ForeignKey(Category, related_name='bundles')
	name = models.CharField(max_length=255, unique=True)
	description = models.TextField()
	image = ThumbnailerImageField(resize_source=dict(size=(80, 80), sharpen=True),
		default=settings.MEDIA_ROOT+'/default.jpg')
	user = models.ForeignKey(User, related_name='bundles')

	def __str__(self):
		return self.name

	def get_data(self):
		thumbnailer = get_thumbnailer(self.image)
		thumbnail_options = {'crop': True, 'size': (80, 80)}
		return {
			'key': self.pk,
			'name': self.name,
			'description': self.description,
			'image': thumbnailer.get_thumbnail(thumbnail_options).url,
		}


@receiver(post_save, sender='auth.User')
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)