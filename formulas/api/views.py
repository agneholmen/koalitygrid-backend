from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from formulas.models import CalculationTool, ConversionTool, Term
from .serializers import CalculationToolSerializer, ConversionToolSerializer, TermNameSerializer, TermDetailSerializer
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
    permission_classes = [AllowAny]

    def get(self, request):
        name_query = request.GET.get('q', '').strip()
        tag_query = request.GET.get('tag', '').strip()
        
        if not name_query and not tag_query:
            return Response([])
        
        queryset = Term.objects.all()
        
        if name_query:
            queryset = queryset.filter(Q(name__icontains=name_query))
        
        if tag_query:
            queryset = queryset.filter(Q(tags__name__icontains=tag_query))
        
        terms = queryset.distinct()[:10]
        serializer = TermNameSerializer(terms, many=True)
        return Response(serializer.data)
    
class TermListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        terms = Term.objects.all().order_by('name')
        serializer = TermNameSerializer(terms, many=True)
        return Response(serializer.data)
    
class TermDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        try:
            term = Term.objects.get(pk=id)
            serializer = TermDetailSerializer(term)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Term.DoesNotExist:
            return Response({'error': 'Finns ingen term med denna ID.'}, status=status.HTTP_400_BAD_REQUEST)

