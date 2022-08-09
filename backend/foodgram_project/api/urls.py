from django.urls import include, path
from rest_framework import routers

from .views import IngredientsViewSet, RecipeViewSet, TagViewSet, UserViewSet

router_v1_0 = routers.DefaultRouter()
router_v1_0.register('recipes', RecipeViewSet, basename='recipes')
router_v1_0.register('tags', TagViewSet, basename='tags')
router_v1_0.register('ingredients', IngredientsViewSet, basename='ingredients')
# router_v1_0.register('users', UserViewSet, 'users')

urlpatterns = [
    path('', include(router_v1_0.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
