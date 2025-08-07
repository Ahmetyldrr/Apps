from django.contrib import admin
from .models import ForecastData, ModelPerformance

@admin.register(ForecastData)
class ForecastDataAdmin(admin.ModelAdmin):
    list_display = ['date', 'actual_value', 'predicted_value', 'error', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['date']
    ordering = ['-date']

@admin.register(ModelPerformance)
class ModelPerformanceAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'r2_score', 'mae', 'rmse', 'created_at']
    list_filter = ['model_name', 'created_at']
    ordering = ['-created_at']
