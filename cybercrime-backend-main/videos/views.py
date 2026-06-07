from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Video, VideoProgress
from .serializers import VideoSerializer, VideoProgressSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from quizzes.models import QuizQuestion  
from quizzes.selectors import quiz_list_random
from quizzes.serializers import QuizQuestionSerializer
import random
import re
from leaderboard.services import (
    award_points,
    award_video_completion
)


class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'id'
    lookup_value_regex = '[^/]+' 


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='max_time',
            description='Maximum duration in minutes',
            required=False,
            type=int
        ),
        OpenApiParameter(
            name='min_time',
            description='Minimum duration in minutes',
            required=False,
            type=int
        )
    ],
    responses=VideoSerializer(many=True)
)
class VideoFilterView(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        queryset = Video.objects.all()
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
    
    
class VideoProgressView(generics.RetrieveUpdateAPIView):
    serializer_class = VideoProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        video_id = self.kwargs['id']
        video = get_object_or_404(Video, pk=video_id)
        obj, _ = VideoProgress.objects.get_or_create(user_id=user, video_id=video)
        return obj

    def perform_update(self, serializer):
        progress = serializer.save()

        video = progress.video_id
        award_video_completion(self.request.user, video)
    

class RelatedContentApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id):
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)

        # Normalize video type and extract keyword
        type_lower = video.type.lower()
        keyword = None
        if "harassment" in type_lower:
            keyword = "Harassment"
        elif "scam" in type_lower:
            keyword = "Scam"
        elif "privacy" in type_lower:
            keyword = "Privacy"

        # --- Related Videos ---
        related_videos = Video.objects.none()
        if keyword:
            related_videos = Video.objects.filter(type__icontains=keyword).exclude(id=video.id)
        sampled_videos = random.sample(list(related_videos), min(2, related_videos.count()))
        videos_data = VideoSerializer(sampled_videos, many=True).data

        # --- Related Quiz ---
        quiz_data = None
        if keyword:
            quizzes = quiz_list_random(filters={"category": keyword}, count=1)
            if quizzes.exists():
                quiz_data = QuizQuestionSerializer(quizzes.first()).data

        return Response({
            "related_videos": videos_data,
            "related_quiz": quiz_data
        })
