from django.db import models

class ForecastData(models.Model):
    product_name = models.CharField(max_length=100)
    forecast_date = models.DateField()
    sales_forecast = models.IntegerField()

    def __str__(self):
        return f"{self.product_name} - {self.forecast_date}"
