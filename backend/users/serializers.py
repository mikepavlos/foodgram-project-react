from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status, exceptions

from .models import User, Subscribe
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
            user=self.context.get('request').user.id
        ).exists()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = FIELDS + ('password',)
        read_only_fields = ('id',)


class RecipeMinifiedSerializer(serializers.ModelSerializer):
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
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = FIELDS + (
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = FIELDS

    def validate(self, attrs):
        user = self.context.get('request').user
        author = self.instance
        if author == user:
            raise exceptions.ValidationError(
                {'errors': 'Нельзя подписываться на самого себя.'}
            )
        if Subscribe.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                {'errors': 'Вы уже подписаны на автора.'}
            )
        return attrs

    def get_recipes(self, obj):
        request = self.context.get('request')
        queryset = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        serializer = RecipeMinifiedSerializer(
            queryset,
            many=True
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
