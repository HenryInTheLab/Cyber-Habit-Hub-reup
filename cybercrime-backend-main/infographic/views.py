from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .models import Victimisation, OnlineBehaviour, FinancialLoss
from .serializers import VictimisationSerializer, OnlineBehaviourSerializer, FinancialLossSerializer


class VictimisationFilterView(APIView):
    @extend_schema(
        description="Filter Victimisation by age, gender, tab, and year (2023 or 2024). Returns only adjusted value for selected year.",
        parameters=[
            OpenApiParameter(name='age', type=OpenApiTypes.STR, description='Age group'),
            OpenApiParameter(name='gender', type=OpenApiTypes.STR, description='Gender'),
            OpenApiParameter(name='tab', type=OpenApiTypes.STR, description='Tab category'),
            OpenApiParameter(name='year', type=OpenApiTypes.STR, description='2023 or 2024'),
        ],
        responses={200: VictimisationSerializer(many=True)}
    )
    def get(self, request):
        queryset = Victimisation.objects.all()
        age = request.query_params.get('age')
        gender = request.query_params.get('gender')
        tab = request.query_params.get('tab')
        year = request.query_params.get('year')

        if age:
            queryset = queryset.filter(age__iexact=age)
        if gender:
            queryset = queryset.filter(gender__iexact=gender)
        if tab:
            queryset = queryset.filter(tab__iexact=tab)

        if year == '2023':
            queryset = queryset.exclude(adjusted_2023__isnull=True)
        elif year == '2024':
            queryset = queryset.exclude(adjusted_2024__isnull=True)

        serializer = VictimisationSerializer(queryset, many=True)
        data = serializer.data

        # Remove the field not requested
        for row in data:
            if year == '2023':
                row.pop('adjusted_2024', None)
            elif year == '2024':
                row.pop('adjusted_2023', None)

        return Response(data)



class OnlineBehaviourFilterView(APIView):
    @extend_schema(
        description="Filter Online Behaviour data and return only selected year's value.",
        parameters=[
            OpenApiParameter(name='age', type=OpenApiTypes.STR),
            OpenApiParameter(name='gender', type=OpenApiTypes.STR),
            OpenApiParameter(name='behaviour_type', type=OpenApiTypes.STR),
            OpenApiParameter(name='tech_level', type=OpenApiTypes.STR),
            OpenApiParameter(name='year', type=OpenApiTypes.STR, description='2023 or 2024'),
        ],
        responses={200: OnlineBehaviourSerializer(many=True)}
    )
    def get(self, request):
        queryset = OnlineBehaviour.objects.all()
        age = request.query_params.get('age')
        gender = request.query_params.get('gender')
        behaviour_type = request.query_params.get('behaviour_type')
        tech_level = request.query_params.get('tech_level')
        year = request.query_params.get('year')

        if age:
            queryset = queryset.filter(age__iexact=age)
        if gender:
            queryset = queryset.filter(gender__iexact=gender)
        if behaviour_type:
            queryset = queryset.filter(behaviour_type__icontains=behaviour_type)
        if tech_level:
            queryset = queryset.filter(tech_level__iexact=tech_level)

        if year == '2023':
            queryset = queryset.exclude(adjusted_2023__isnull=True)
        elif year == '2024':
            queryset = queryset.exclude(adjusted_2024__isnull=True)

        serializer = OnlineBehaviourSerializer(queryset, many=True)
        data = serializer.data

        # Hide the unselected year
        for row in data:
            if year == '2023':
                row.pop('adjusted_2024', None)
            elif year == '2024':
                row.pop('adjusted_2023', None)

        return Response(data)



@extend_schema(
    description="Filter Financial Loss data by median_type and cybercrime.",
    parameters=[
        OpenApiParameter(name='median_type', type=OpenApiTypes.STR, description='e.g. "Consumer" or "SME"'),
        OpenApiParameter(name='cybercrime', type=OpenApiTypes.STR, description='e.g. "Scam", "Hacking"'),
    ],
    responses={200: FinancialLossSerializer(many=True)}
)
class FinancialLossFilterView(APIView):
    def get(self, request):
        queryset = FinancialLoss.objects.all()
        median_type = request.query_params.get('median_type')
        cybercrime = request.query_params.get('cybercrime')

        if median_type:
            queryset = queryset.filter(median_type__icontains=median_type)
        if cybercrime:
            queryset = queryset.filter(cybercrime__icontains=cybercrime)

        serializer = FinancialLossSerializer(queryset, many=True)
        return Response(serializer.data)
