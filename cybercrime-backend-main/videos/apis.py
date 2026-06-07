from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Video
from .serializers import VideoSerializer

class VideoListApi(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class VideoDetailApi(RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
