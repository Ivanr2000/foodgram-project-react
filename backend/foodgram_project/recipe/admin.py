from django.contrib import admin

from .models import (Favorites, Follow, Ingredient, Recipe, RecipeIngredient,
                     RecipeTag, ShoppingCart, Tag, UnitOfMeasurement)


class UnitOfMeasurementAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'color',
                    'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3


class TagsInline(admin.TabularInline):
    model = RecipeTag
    extra = 3


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientsInline, TagsInline,)
    list_display = ('pk',
                    'name',
                    'image',
                    'text',
                    'author',
                    'cooking_time',
                    'favorites_count',)
    search_fields = ('name', 'author', 'ingredients',)
    list_filter = ('name', 'tags', 'author', )
    empty_value_display = '-пусто-'

    def favorites_count(self, obj):
        return obj.favorites.count()


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'recipe',
                    'ingredient',
                    'amount',)
    search_fields = ('recipe', 'ingredient',)
    list_filter = ('ingredient',)
    empty_value_display = '-пусто-'


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'recipe',
                    'tag',)
    search_fields = ('tag',)
    empty_value_display = '-пусто-'


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'user',
                    'recipe',)
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'user',
                    'author',)
    search_fields = ('user', 'author',)
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'user',
                    'recipe',)
    search_fields = ('user', 'recipe',)
    empty_value_display = '-пусто-'


admin.site.register(UnitOfMeasurement, UnitOfMeasurementAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
