from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class EnergyMarketData(models.Model):
    SMF_DIRECTION_CHOICES = [
        ('enerji_acigi', 'Enerji Açığı'),
        ('enerji_fazlasi', 'Enerji Fazlası'),
        ('dengede', 'Dengede'),
    ]
    
    date = models.DateField()
    hour = models.TimeField()
    ptf = models.FloatField(verbose_name='PTF (TL/MWh)', help_text='Piyasa Takas Fiyatı')
    smf = models.FloatField(verbose_name='SMF (TL/MWh)', help_text='Sistem Marjinal Fiyatı')
    positive_imbalance_price = models.FloatField(verbose_name='Pozitif Dengesizlik Fiyatı (TL/MWh)')
    negative_imbalance_price = models.FloatField(verbose_name='Negatif Dengesizlik Fiyatı (TL/MWh)')
    smf_direction = models.CharField(max_length=20, choices=SMF_DIRECTION_CHOICES, verbose_name='SMF Yön')
    predicted_smf_direction = models.CharField(max_length=20, choices=SMF_DIRECTION_CHOICES, null=True, blank=True, verbose_name='Tahmin Edilen SMF Yön')
    prediction_confidence = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)], verbose_name='Tahmin Güvenilirliği')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date', 'hour']
        unique_together = ['date', 'hour']
        verbose_name = 'Enerji Piyasası Verisi'
        verbose_name_plural = 'Enerji Piyasası Verileri'
    
    def __str__(self):
        return f"{self.date} {self.hour} - PTF: {self.ptf}, SMF: {self.smf}, Yön: {self.get_smf_direction_display()}"

class ForecastData(models.Model):
    date = models.DateField()
    actual_value = models.FloatField(null=True, blank=True)
    predicted_value = models.FloatField(null=True, blank=True)
    error = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = [['date']]  # Tuple olarak düzeltildi
        verbose_name = 'Tahmin Verisi'
        verbose_name_plural = 'Tahmin Verileri'
    
    def __str__(self):
        return f"{self.date} - Actual: {self.actual_value}, Predicted: {self.predicted_value}"

class ModelPerformance(models.Model):
    MODEL_CHOICES = [
        ('linear', 'Linear Regression'),
        ('polynomial', 'Polynomial Regression'),
        ('arima', 'ARIMA'),
        ('exponential', 'Exponential Smoothing'),
        ('lstm', 'LSTM Neural Network'),
        ('random_forest', 'Random Forest'),
    ]
    
    model_name = models.CharField(max_length=50, choices=MODEL_CHOICES)
    mae = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Mean Absolute Error')
    mse = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Mean Squared Error')
    rmse = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Root Mean Squared Error')
    r2_score = models.FloatField(validators=[MinValueValidator(-1), MaxValueValidator(1)], verbose_name='R² Score')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Model Performansı'
        verbose_name_plural = 'Model Performansları'
    
    def __str__(self):
        return f"{self.get_model_name_display()} - R²: {self.r2_score:.3f}" # type: ignore

class AIAnalysis(models.Model):
    ANALYSIS_TYPES = [
        ('data_trends', 'Veri Trend Analizi'),
        ('model_performance', 'Model Performans Değerlendirmesi'),
        ('forecast_insights', 'Tahmin Öngörüleri'),
        ('energy_market_analysis', 'Enerji Piyasası Analizi'),
    ]
    
    analysis_type = models.CharField(max_length=50, choices=ANALYSIS_TYPES, verbose_name='Analiz Türü')
    content = models.TextField(verbose_name='İçerik')
    status = models.CharField(max_length=20, default='success', verbose_name='Durum')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'AI Analizi'
        verbose_name_plural = 'AI Analizleri'
    
    def __str__(self):
        return f"{self.get_analysis_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
