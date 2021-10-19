from bboard.models import Bb
from comments.models import Comment
from rest_framework import serializers


class BbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = (
            "id",
            "title",
            "content",
            "price",
            "created_at",
        )


class BbDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "bb",
            "author",
            "content",
            "created_at",
        )
