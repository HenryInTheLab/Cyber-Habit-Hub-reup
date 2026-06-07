from django.urls import path
from .views import ArticleListAPIView, ArticleFilterView, record_article_click

urlpatterns = [
    path('', ArticleListAPIView.as_view(), name='article-list'),
    path('filter/', ArticleFilterView.as_view(), name='article-filter'),
    path("<str:article_id>/click/", record_article_click, name="article-click"),
]
