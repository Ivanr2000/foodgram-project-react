from drf_extra_fields.fields import Base64ImageField
from recipe.models import (Ingredient, Recipe, RecipeIngredient, Tag,
                           UnitOfMeasurement)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import CustomUser


class UnitOfMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasurement
        fields = 'name'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.SlugRelatedField(
        slug_field='name', queryset=UnitOfMeasurement.objects.all()
    )

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInReceipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    # measurement_unit = IngredientSerializer(source='ingredient')
    # ingredient = serializers.SlugRelatedField(
    #     slug_field='name', queryset=UnitOfMeasurement.objects.all()
    # )
    # measurement_unit = serializers.ReadOnlyField(source='ingredients.measurement_unit')
    measurement_unit = serializers.ReadOnlyField(source='recipeingredients.get_measurement_unit')
    # measurement_unit = serializers.ModelField(model_field=UnitOfMeasurement()._meta.get_field('name'))

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=RecipeIngredient.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInReceipeSerializer(
        source='recipeingredients',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = '__all__'
