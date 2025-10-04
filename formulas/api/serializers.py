from rest_framework import serializers
from formulas.models import CalculationTool, ConversionTool

class CalculationToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationTool
        fields = [
            "id",
            "name",
            "description",
            "formula_info",
            "component",
        ]

class ConversionToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionTool
        fields = [
            "id",
            "name",
            "description",
            "formula_info",
            "component",
        ]