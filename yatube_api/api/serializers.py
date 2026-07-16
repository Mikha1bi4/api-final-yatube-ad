from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post, Group, Follow


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    posts = PostSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description', 'posts')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    following = serializers.StringRelatedField()

    class Meta:
        model = Follow
        fields = ('user', 'following')
