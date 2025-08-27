from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Api
from .serializers import ApiSerializer

class ApiViewSet(viewsets.ModelViewSet):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# API Views (REST)
class ApiListView(generics.ListAPIView):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApiDetailView(generics.RetrieveAPIView):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApiCreateView(generics.CreateAPIView):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ApiUpdateView(generics.UpdateAPIView):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Api.objects.filter(user=self.request.user)

class ApiDeleteView(generics.DestroyAPIView):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Api.objects.filter(user=self.request.user)

# Template Views
class ApiListTemplateView(LoginRequiredMixin, ListView):
    model = Api
    template_name = 'apis/api_list.html'
    context_object_name = 'apis'
    paginate_by = 10

class ApiDetailTemplateView(LoginRequiredMixin, DetailView):
    model = Api
    template_name = 'apis/api_detail.html'
    context_object_name = 'api'

class ApiCreateTemplateView(LoginRequiredMixin, CreateView):
    model = Api
    template_name = 'apis/api_form.html'
    fields = ['name', 'description', 'endpoint']
    success_url = reverse_lazy('api-list-template')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ApiUpdateTemplateView(LoginRequiredMixin, UpdateView):
    model = Api
    template_name = 'apis/api_form.html'
    fields = ['name', 'description', 'endpoint']
    success_url = reverse_lazy('api-list-template')
    
    def get_queryset(self):
        return Api.objects.filter(user=self.request.user)

class ApiDeleteTemplateView(LoginRequiredMixin, DeleteView):
    model = Api
    template_name = 'apis/api_confirm_delete.html'
    success_url = reverse_lazy('api-list-template')
    
    def get_queryset(self):
        return Api.objects.filter(user=self.request.user)