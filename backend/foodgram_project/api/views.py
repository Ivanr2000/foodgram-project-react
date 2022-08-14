import datetime

from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from recipe.models import (Favorites, Follow, Ingredient, Recipe,
                           RecipeIngredient, ShoppingCart, Tag)
from rest_framework import permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser

from .filters import IngredientSearchFilter, RecipeFilter
from .mixins import ListRetriveViewSet
from .permissions import AdminOrReadOnly, AuthorAdminOrReadOnly
from .serializers import (AddRecipeSerializer, FavoritesSerializer,
                          FollowSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)


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


class TagViewSet(ListRetriveViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AdminOrReadOnly,)
    pagination_class = None


class IngredientsViewSet(ListRetriveViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class SubscriptionsViewSet(viewsets.ModelViewSet):
    """
    Класс формирует ответы для эндпойнта со списком подписок - subscriptions.
    """
    queryset = Follow.objects.all()
    permission_classes = (AuthorAdminOrReadOnly,)

    def list(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class FollowFavoriteCartView(APIView):
    """
    Класс формирует ответы для эндпойнтов: подписки на пользователя -
    subscribe (необходимо передать автора), избранных рецептов -
    favorite (необходимо передать рецепт), и корзины покупок -
    shopping_cart (необходимо передать рецепт). Ответ определяется исходя из
    переданного пути. Класс реализует добавление объектов по указанным
    эндпойнтам и их удаление.
    """
    permission_classes = (AuthorAdminOrReadOnly,)

    URLSERIALIZERS = {
        'subscribe': {
            'serializer': FollowSerializer,
            'follow_model': CustomUser,
            'data': 'author',
            'model_delete': Follow,
        },
        'favorite': {
            'serializer': FavoritesSerializer,
            'follow_model': Recipe,
            'data': 'recipe',
            'model_delete': Favorites,
        },
        'shopping_cart': {
            'serializer': ShoppingCartSerializer,
            'follow_model': Recipe,
            'data': 'recipe',
            'model_delete': ShoppingCart,
        },
    }

    def post(self, request, id=None):
        user = request.user
        endpoint = request.get_full_path().split('/')[-2]
        object_for_follow = get_object_or_404(
            self.URLSERIALIZERS[endpoint]['follow_model'],
            id=self.kwargs.get('id')
        )
        data = {
            'user': user.id,
            self.URLSERIALIZERS[endpoint]['data']: object_for_follow.id,
        }
        serializer = self.URLSERIALIZERS[endpoint]['serializer'](
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id=None):
        user = request.user
        endpoint = request.get_full_path().split('/')[-2]
        following_object = get_object_or_404(
            self.URLSERIALIZERS[endpoint]['follow_model'],
            id=self.kwargs.get('id')
        )

        if endpoint == 'subscribe':
            if user == following_object:
                return Response({
                    'errors': 'Вы не можете отписываться от самого себя'
                }, status=status.HTTP_400_BAD_REQUEST)

            object_for_deletion = get_object_or_404(
                self.URLSERIALIZERS[endpoint]['model_delete'],
                user=user,
                author=following_object
            )
        else:
            object_for_deletion = get_object_or_404(
                self.URLSERIALIZERS[endpoint]['model_delete'],
                user=user,
                recipe=following_object
            )
        object_for_deletion.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(APIView):
    """
    Класс формирует ответы для эндпойнта - download_shopping_cart. Сумирует
    все одинаковые ингредиенты и выводит их в файл формата txt. На текущий
    момент после вывода списка корзина покупок неопустошается, так как
    фронтенд не поддерживает запрос подтверждения удаления позиций из корзины.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        shopping_cart = {}

        ingredients = RecipeIngredient.objects.filter(
            recipe__shoppingcarts__user=user
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

        shopping_list = [
            'Список покупок сформирован с помощью проекта Foodgram\n']
        shopping_list.append(
            'Дата формирования списка: '
            f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}\n\n'
        )

        for ingredient, value in shopping_cart.items():
            shopping_list.append(
                f' {ingredient} - {value["amount"]} '
                f'{value["measurement_unit"]}\n'
            )

        response = HttpResponse(shopping_list, {
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename="shopping_list.txt"',
        })
        return response
