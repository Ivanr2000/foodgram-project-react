from django.urls import include, path
from rest_framework import routers

from .views import (IngredientsViewSet, RecipeViewSet, TagViewSet,
                    UserSubscribeViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register('users', UserSubscribeViewSet, basename='users')

urlpatterns = [
    path(
        'users/subscriptions/',
        UserSubscribeViewSet.as_view({'get': 'subscriptions', }),
        name='subscriptions'
    ),
    path('', include('djoser.urls')),
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
