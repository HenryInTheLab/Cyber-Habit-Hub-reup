from rest_framework import serializers
from .models import Victimisation, OnlineBehaviour, FinancialLoss

class VictimisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victimisation
        fields = '__all__'

class OnlineBehaviourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineBehaviour
        fields = '__all__'

class FinancialLossSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialLoss
        fields = '__all__'
