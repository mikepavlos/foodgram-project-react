from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram.pagination import Paginator
from .models import Subscribe, User
from .serializers import UserWithRecipesSerializer


class UserViewSet(DjoserUserViewSet):
    pagination_class = Paginator
    http_method_names = ('get', 'post')

    @action(
        http_method_names=['post', 'delete'],
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        user = request.user
        if request.method == 'POST':
            author = get_object_or_404(User, id=id)
            if author == user:
                return Response(
                    {'errors': 'Нельзя подписываться на самого себя.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            _, create = Subscribe.objects.get_or_create(
                user=user,
                author=author
            )
            if not create:
                return Response(
                    {'errors': 'Вы уже подписаны на автора.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = UserWithRecipesSerializer(
                author,
                context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        subscription = Subscribe.objects.filter(user=user, author__id=id)
        if not subscription.exists():
            return Response(
                {'errors': 'Подписка не найдена.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = UserWithRecipesSerializer(
            page,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)
