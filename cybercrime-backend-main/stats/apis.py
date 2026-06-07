from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from stats.selectors import stats_get
from stats.serializers import StatsSerializer


class StatsApi(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=StatsSerializer,
        description="Fetches the user's stats."
    )
    def get(self, request):
        stats = stats_get(request.user.id)
        serializer = StatsSerializer(stats)
        return Response(serializer.data)
