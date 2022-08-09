from django.shortcuts import render
from recipe.models import Ingredient, Recipe, Tag
from rest_framework import filters, permissions, status, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from users.models import CustomUser

from .mixins import ListRetriveViewSet
from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, UserSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = PageNumberPagination
    serializer_class = RecipeSerializer

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return TitlesSerializerGet
    #     return TitlesSerializer


class TagViewSet(ListRetriveViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    http_method_names = ('get',)


class IngredientsViewSet(ListRetriveViewSet):
    # permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class UserViewSet(ListRetriveViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    http_method_names = ('get',)
