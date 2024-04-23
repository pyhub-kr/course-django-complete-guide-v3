from django.db.models import QuerySet
from rest_framework import serializers
from accounts.models import User
from .models import Post, Comment


class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, user) -> str:
        return f"{user.last_name} {user.first_name}".strip()

    class Meta:
        model = User
        fields = ["id", "username", "email", "name"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "message"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content"]


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = ["id", "title", "author"]

    @staticmethod
    def get_optimized_queryset() -> QuerySet[Post]:
        return Post.objects.all().only("id", "title", "author").select_related("author")


class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    comment_list = CommentSerializer(source="comment_set", many=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "comment_list"]

    @staticmethod
    def get_optimized_queryset() -> QuerySet[Post]:
        return Post.objects.all()
