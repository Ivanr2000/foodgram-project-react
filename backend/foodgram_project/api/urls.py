from django.urls import include, path, re_path
from rest_framework import routers

from .views import (DownloadShoppingCart, FollowFavoriteCartView,
                    IngredientsViewSet, RecipeViewSet, SubscriptionsViewSet,
                    TagViewSet)

router_v1_0 = routers.DefaultRouter()
router_v1_0.register('recipes', RecipeViewSet, basename='recipes')
router_v1_0.register('tags', TagViewSet, basename='tags')
router_v1_0.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1_0.register(
    'users/subscriptions', SubscriptionsViewSet, basename='subscriptions'
)

urlpatterns = [
    re_path(
        r'users/(?P<id>[0-9]+)/subscribe/',
        FollowFavoriteCartView.as_view(),
    ),
    re_path(
        r'recipes/(?P<id>[0-9]+)/favorite/',
        FollowFavoriteCartView.as_view(),
    ),
    re_path(
        r'recipes/(?P<id>[0-9]+)/shopping_cart/',
        FollowFavoriteCartView.as_view(),
    ),
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCart.as_view(),
    ),
    path('', include(router_v1_0.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
