from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^categories/$', views.get_categories, name='get_categories'),
    url(r'^categories/(?P<category_key>[0-9]+)/bundles/$', views.handle_request_for_bundles, name='bundles'),
]
