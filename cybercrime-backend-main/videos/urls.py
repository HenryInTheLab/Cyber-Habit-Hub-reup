from django.urls import path
from .views import VideoListView, VideoDetailView, VideoFilterView, VideoProgressView, RelatedContentApi

urlpatterns = [
    path('', VideoListView.as_view(), name='video-list'),
    path('filter/', VideoFilterView.as_view(), name="video-filter"),
    path('<str:id>/progress/', VideoProgressView.as_view(), name='video-progress'),
    path('<str:video_id>/related/', RelatedContentApi.as_view(), name='related-content'),
    path('<id>/', VideoDetailView.as_view(), name='video-detail'),
]
