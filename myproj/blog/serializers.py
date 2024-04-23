from rest_framework import serializers
from accounts.models import User
from .models import Post


class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, user) -> str:
        return f"{user.last_name} {user.first_name}".strip()

    class Meta:
        model = User
        fields = ["id", "username", "email", "name"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content"]


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = ["id", "title", "author"]


class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    comment_list = serializers.StringRelatedField(source="comment_set", many=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "comment_list"]
