import random
from datetime import date, timedelta
import pandas as pd
import io

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ForecastData
from .serializers import ForecastDataSerializer

def generate_synthetic_data():
    """Generates synthetic forecast data."""
    product_names = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    data = []
    start_date = date.today()

    for _ in range(100): # Generate 100 random data points
        product_name = random.choice(product_names)
        forecast_date = start_date + timedelta(days=random.randint(1, 90))
        sales_forecast = random.randint(50, 1000)
        
        # Create and save model instance
        forecast_instance = ForecastData.objects.create(
            product_name=product_name,
            forecast_date=forecast_date,
            sales_forecast=sales_forecast
        )
        data.append({
            'product_name': forecast_instance.product_name,
            'forecast_date': forecast_instance.forecast_date,
            'sales_forecast': forecast_instance.sales_forecast,
        })
    return data

from django.views.generic import TemplateView
from django.shortcuts import redirect

class GenerateForecastView(APIView):
    """
    An API view to generate synthetic forecast data and save it.
    """
    def get(self, request, *args, **kwargs):
        # 1. Clear old data
        ForecastData.objects.all().delete()

        # 2. Generate synthetic data and save it
        generate_synthetic_data()

        # 3. Redirect to the dashboard
        return redirect('forecast-dashboard')

class DownloadForecastView(APIView):
    """
    An API view to provide a download link for an Excel file
    with the current forecast data.
    """
    def get(self, request, *args, **kwargs):
        # 1. Get data from database
        queryset = ForecastData.objects.all().order_by('-forecast_date')
        data = list(queryset.values('product_name', 'forecast_date', 'sales_forecast'))

        if not data:
            return HttpResponse("No data available to download.", status=404)

        # 2. Create a pandas DataFrame
        df = pd.DataFrame(data)

        # 3. Create an in-memory Excel file
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Forecast', index=False)
        
        output.seek(0)

        # 4. Create the HTTP response for file download
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="forecast_data.xlsx"'

        return response

class ForecastDashboardView(TemplateView):
    template_name = 'data_generator/forecast_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forecasts'] = ForecastData.objects.all().order_by('-forecast_date')
        return context

