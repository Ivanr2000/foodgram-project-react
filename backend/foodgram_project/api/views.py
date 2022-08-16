import datetime

from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (
    LimitOffsetPagination, PageNumberPagination,
)
from rest_framework.response import Response

from recipes.models import (
    Favorites, Follow, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag
)
from users.models import CustomUser
from .filters import IngredientSearchFilter, RecipeFilter
from .mixins import ListRetriveViewSet
from .permissions import AdminOrReadOnly, AuthorAdminOrReadOnly
from .serializers import (
    AddRecipeSerializer, FavoritesSerializer, FollowSerializer,
    IngredientSerializer, RecipeSerializer, ShoppingCartSerializer,
    TagSerializer, UserSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return AddRecipeSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated, ],
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = {}

        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_carts__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit_id__name'
        ).annotate(
            Sum('amount')
        )

        for ingredient in ingredients:
            shopping_cart[ingredient['ingredient__name']] = {
                'amount': ingredient['amount__sum'],
                'measurement_unit': ingredient[
                    'ingredient__measurement_unit_id__name'
                ]
            }

        current_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        shopping_list = (
            'Список покупок сформирован с помощью проекта Foodgram\n'
            f'Дата формирования списка: {current_date}\n\n'
        )

        for ingredient, value in shopping_cart.items():
            shopping_list = shopping_list + (
                f' {ingredient} - {value["amount"]} '
                f'{value["measurement_unit"]}\n'
            )

        return HttpResponse(shopping_list, {
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename="shopping_list.txt"',
        })

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticatedOrReadOnly, ],
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            data = {
                'user': user.id,
                'recipe': recipe.id,
            }
            serializer = FavoritesSerializer(
                data=data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        Favorites.objects.filter(
            user=user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticatedOrReadOnly, ]
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            data = {
                'user': user.id,
                'recipe': recipe.id,
            }
            serializer = ShoppingCartSerializer(
                data=data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        ShoppingCart.objects.filter(
            user=user, recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(ListRetriveViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AdminOrReadOnly,)


class IngredientsViewSet(ListRetriveViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class UserSubscribeViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorAdminOrReadOnly,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(CustomUser, pk=pk)

        if request.method == 'POST':
            data = {
                'user': user.id,
                'author': author.id,
            }
            serializer = FollowSerializer(
                data=data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if user == author:
            return Response({
                'errors': 'Вы не можете отписываться от самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = get_object_or_404(
            Follow, user=user, author=author
        )
        follow.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['GET', ],
        permission_classes=[permissions.IsAuthenticated, ],
        url_path='subscriptions'
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
