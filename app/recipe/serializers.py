from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from core.models import Tag, Ingredient, Recipe


class TagSerializer(ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(ModelSerializer):
    """Serializer for ingredient object"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(ModelSerializer):
    """Serializer for recipe object"""
    ingredients = PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients',
                  'tags', 'time_minutes', 'price', 'link')
        read_only_fields = ('id',)
