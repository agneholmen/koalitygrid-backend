from django.urls import path
from .views import CalculationToolListView, ConversionToolListView, SearchTermsView, TermDetailView, TermListView

urlpatterns = [
    path('calculation-tools/', CalculationToolListView.as_view(), name='calculation-tool-list'),
    path('conversion-tools/', ConversionToolListView.as_view(), name='conversion-tool-list'),
    path('terms/search/', SearchTermsView.as_view(), name='search-terms'),
    path('terms/list/', TermListView.as_view(), name='terms-list'),
    path('terms/<int:id>/', TermDetailView.as_view(), name='term-detail'),
]