from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "type",
            "title",
            "author",
            "publish_date",
            "description",
            "link",
            "suggested_reading_time",
            "created_at",
            "thumbnail_url",
        ]
