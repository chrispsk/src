from rest_framework import serializers
from accounts.models import Tag, Ingredient, Reteta


class TagSerializer(serializers.ModelSerializer):
    """"Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """"Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RetetaSerializer(serializers.ModelSerializer):
    """"Serializer for reteta objects"""
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Reteta
        fields = ('id', 'title', 'ingredients', 'tags',
                  'time_minutes', 'price', 'link'
                  )
        read_only_fields = ('id',)


class RetetaDetailSerializer(RetetaSerializer):
    """"Serializer for reteta details"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
