from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from .models import Subscribe, User
from recipes.models import Recipe

FIELDS = ('email', 'id', 'username', 'first_name', 'last_name',)


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = FIELDS + ('is_subscribed',)
        read_only_fields = ('id', 'is_subscribed')

    def get_is_subscribed(self, obj):
        return obj.subscribing.filter(
            user=self.context.get('request').user
        ).exists()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = FIELDS + ('password',)
        read_only_fields = ('id',)


class RecipeMiniFieldSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = fields


class UserWithRecipesSerializer(UserSerializer):
    recipes = RecipeMiniFieldSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = FIELDS + (
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

