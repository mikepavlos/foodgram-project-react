from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .serializers import (
    IngredientSerializer,
    RecipeListSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerializer
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'get':
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @staticmethod
    def add_to_list(model, user, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        _, create = model.objects.get_or_create(
            user=user,
            recipe=recipe
        )
        if not create:
            return Response(
                {'errors': 'Дублирование добавления.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RecipeListSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_from_list(model, user, pk):
        instance = model.objects.filter(user=user, recipe__id=pk)
        if not instance.exists():
            return Response(
                {'errors': 'Рецепт отсутствует в списке.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to_list(Favorite, request.user, pk)
        return self.delete_from_list(Favorite, request.user, pk)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to_list(ShoppingCart, request.user, pk)
        return self.delete_from_list(ShoppingCart, request.user, pk)
