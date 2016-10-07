from django.shortcuts import render
from .models import Category
from django.http import JsonResponse
from .forms import BundleForm


def get_categories(request):
    data = [category.get_data() for category in Category.objects.all()]

    return JsonResponse(data, safe=False)


def handle_request_for_bundles(request, category_key):
    if request.method == 'POST':
        form = BundleForm(request.POST, request.FILES)
        if form.is_valid():
            category = Category.objects.get(pk=category_key)
            bundle = form.save(commit=False)
            bundle.category = category
            bundle.save()

    return JsonResponse({'ok': True})