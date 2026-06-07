# infographic/urls.py
from django.urls import path
from .views import VictimisationFilterView, OnlineBehaviourFilterView, FinancialLossFilterView

urlpatterns = [
    path('victimisation/', VictimisationFilterView.as_view(), name='victimisation-list'),
    path('online-behaviours/', OnlineBehaviourFilterView.as_view(), name='online-behaviours-list'),
    path('financial-losses/', FinancialLossFilterView.as_view(), name='financial-losses-list'),
]
