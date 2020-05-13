from rest_framework import serializers
from .models import *

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    sub_comments_set = RecursiveField(many=True, read_only=True)
    total_likes = serializers.ReadOnlyField()
    total_dislikes = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'total_likes', 'total_dislikes', 'sub_comments_set']

class LikeSerializer(serializers.ModelSerializer):
    comment = serializers.ReadOnlyField(source='comment.comment')
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Like
        fields = ['id', 'comment', 'user']

class DisLikeSerializer(serializers.ModelSerializer):
    comment = serializers.ReadOnlyField(source='comment.comment')
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Like
        fields = ['id', 'comment', 'user']
