from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from apps.apis.models import Api

User = get_user_model()

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_apis'] = Api.objects.order_by('-created_at')[:6]
        context['total_apis'] = Api.objects.count()
        context['total_users'] = User.objects.count()
        return context