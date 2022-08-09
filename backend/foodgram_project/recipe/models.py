from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.constraints import UniqueConstraint

User = get_user_model()


class UnitOfMeasurement(models.Model):
    name = models.CharField(
        'Единица измерения',
        max_length=20,
        unique=True,
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return "%s" % (self.name)


class Ingredient(models.Model):
    name = models.CharField(
        'Ингредиент',
        max_length=150,
        db_index=True,
    )
    measurement_unit = models.ForeignKey(
        UnitOfMeasurement,
        related_name='ingredients',
        on_delete=models.CASCADE,
        verbose_name='Единица измерения',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'], name='unique_UOM'
            ),
        ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        'Тэг',
        max_length=200,
        db_index=True,
        unique=True,
    )
    color = ColorField(
        'Цвет',
        max_length=7,
        default='#FF0000',
        )
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        'Рецепт',
        max_length=250,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipe/',
    )
    text = models.TextField(
        'Описание рецепта',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='RecipeIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        through='RecipeTag',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления, в минутах'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField('Вес')

    class Meta:
        verbose_name = 'Состав ингридиентов'
        verbose_name_plural = 'Состав ингридиентов'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_ingredients_recipe')
        ]

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='recipetags',
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        'Tag',
        on_delete=models.CASCADE,
        related_name='recipetags',
        verbose_name='Теги'
    )

    class Meta:
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецептов'

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ['user', 'author']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique follow',
            )
        ]
