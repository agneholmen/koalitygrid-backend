from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from formulas.models import CalculationTool, ConversionTool, Term
from .serializers import CalculationToolSerializer, ConversionToolSerializer, TermSerializer
from rest_framework.permissions import AllowAny
from django.db.models import Q

class CalculationToolListView(ListAPIView):
    serializer_class = CalculationToolSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            CalculationTool.objects
            .filter(enabled=True)
            .exclude(component='')
            .select_related("category")
            .order_by('name')
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        grouped = {}

        for obj in queryset:
            category_name = obj.category.name if obj.category else "no_category"
            serialized = self.get_serializer(obj).data
            grouped.setdefault(category_name, []).append(serialized)

        return Response(grouped)
    
class ConversionToolListView(ListAPIView):
    serializer_class = ConversionToolSerializer
    permission_classes = [AllowAny]
    queryset = ConversionTool.objects.filter(enabled=True).order_by('name')

class SearchTermsView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            terms = Term.objects.filter(Q(name__icontains=query))[:10]
            serializer = TermSerializer(terms, many=True)
            return Response(serializer.data)
        return Response([])