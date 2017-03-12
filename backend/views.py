from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Category, Bundle, Product
from . import serializers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryTile

    def retrieve(self, request, pk=None):
        category = get_object_or_404(self.queryset, pk=pk)
        serializer = serializers.Category(category, context={'request': request})
        return Response(serializer.data)


class BundleViewSet(viewsets.ModelViewSet):
    queryset = Bundle.objects.all()
    parser_classes = (FormParser, MultiPartParser)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BundleTile
        if self.action == 'create':
            return serializers.BundleCreate
        return serializers.Bundle

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.Product


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.User

    @detail_route(methods=['post'])
    def edit(self, request, pk=None):
        if pk != 'current':
            return None

        if not request.user.check_password(request.data['password']):
            return Response('wrong current password', status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if request.data.get('newPassword', default=None):
            request.user.set_password(request.data['newPassword'])
            request.user.save()

        serializer = serializers.EditUser(request.user, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response('Edited user')

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            return self.request.user

        return super(UserViewSet, self).get_object()