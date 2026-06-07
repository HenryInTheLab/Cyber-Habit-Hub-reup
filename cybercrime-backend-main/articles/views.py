from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from .models import Article
from .serializers import ArticleSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from leaderboard.services import award_article_click


class ArticleListAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all().order_by('-publish_date')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='min_time',
            description='Minimum reading time in minutes',
            required=False,
            type=int
        ),
        OpenApiParameter(
            name='max_time',
            description='Maximum reading time in minutes',
            required=False,
            type=int
        ),
    ],
    responses=ArticleSerializer(many=True),
    description="Filter articles by suggested reading time (in minutes)."
)
class ArticleFilterView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all().order_by('-publish_date')
        min_time = self.request.query_params.get('min_time')
        max_time = self.request.query_params.get('max_time')

        try:
            if min_time is not None:
                queryset = queryset.filter(suggested_reading_time__gte=int(min_time))
            if max_time is not None:
                queryset = queryset.filter(suggested_reading_time__lte=int(max_time))
        except ValueError:
            raise ValidationError("min_time and max_time must be integers")

        return queryset
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def record_article_click(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    awarded = award_article_click(request.user, article)
    return Response({"status": "ok", "awarded": awarded})