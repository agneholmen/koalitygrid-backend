from django.contrib import admin

from .models import (
    CalculationTool, CalculationToolCategory, ConversionTool, Document, Favorite, Formula, Template, Term
)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'file', 'uploaded_by', 'created_at', 'updated_at']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'target_ct', 'target_id', 'target', 'created_at']

@admin.register(Formula)
class FormulaAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_by', 'created_at', 'updated_at', 'enabled']

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'file', 'uploaded_by', 'created_at', 'updated_at', 'enabled']

@admin.register(CalculationTool)
class CalculationToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'formula_key', 'component', 'enabled']

@admin.register(CalculationToolCategory)
class CalculationToolCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ConversionTool)
class ConversionToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'formula_info', 'component']

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']