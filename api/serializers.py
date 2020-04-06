from rest_framework.fields import CurrentUserDefault
from rest_framework import serializers

from .models import Post, Like, Unlike


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(default=CurrentUserDefault(), read_only=True)
    likes = serializers.SerializerMethodField()
    unlikes = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'body', 'created_at', 'likes', 'unlikes']

    def get_likes(self, obj):
        return obj.likes.count()
    
    def get_unlikes(self, obj):
        return obj.unlikes.count()


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(default=CurrentUserDefault(), read_only=True)
    post = serializers.CharField(read_only=True)
    class Meta:
        model = Like
        fields = ['author', 'post']


class UnlikeSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(default=CurrentUserDefault(), read_only=True)
    post = serializers.CharField(read_only=True)
    class Meta:
        model = Unlike
        fields = ['author', 'post']