from rest_framework import viewsets, permissions
from posts.models import Post, Comment, Group, Follow, User
from .serializers import (
    PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer)
from rest_framework.pagination import LimitOffsetPagination
from .permitions import OwnerOrReadOnly
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import filters


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.OrderingFilter, )
    # Без сортировки пагинация не будет нормально работать
    ordering_fields = ('pub_date', 'text')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        # Возвращаем только подписки текущего пользователя
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Получаем username из запроса
        following_username = self.request.data.get('following')

        if not following_username:
            raise ValidationError({"following":
                                  "Необходимо указать username"
                                   " пользователя для подписки"}
                                  )
        try:
            following_user = User.objects.get(username=following_username)
        except User.DoesNotExist:
            raise ValidationError({"following":
                                  f"Пользователь с username '{
                                      following_username}' не найден"})

        # Проверка: нельзя подписаться на себя
        if following_user == self.request.user:
            raise ValidationError("Нельзя подписаться на самого себя")

        # Проверка: уже подписан?
        if Follow.objects.filter(user=self.request.user,
                                 following=following_user).exists():
            raise ValidationError("Вы уже подписаны на этого пользователя")

        # Сохраняем
        serializer.save(
            user=self.request.user,
            following=following_user
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly, )

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        if not Post.objects.filter(id=post_id).exists():
            raise NotFound("The post does not exist")

        queryset = Comment.objects.filter(post_id=post_id)

        return queryset

    def perform_create(self, serializer):
        """Автоматически подставляем автора и пост"""
        post_id = self.kwargs.get('post_id')

        if not Post.objects.filter(id=post_id).exists():
            raise NotFound("The post does not exist")

        post = Post.objects.get(id=post_id)

        serializer.save(author=self.request.user, post=post)
