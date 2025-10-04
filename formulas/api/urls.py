from django.urls import path
from .views import CalculationToolListView, ConversionToolListView, search_terms

urlpatterns = [
    path('calculation-tools/', CalculationToolListView.as_view(), name='calculation-tool-list'),
    path('conversion-tools/', ConversionToolListView.as_view(), name='conversion-tool-list'),
    path('terms/search/', search_terms, name='search-terms'),
]