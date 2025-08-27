from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# DRF Router for API endpoints
router = DefaultRouter()
router.register(r'api', views.ApiViewSet)

urlpatterns = [
    # API endpoints (REST)
    path('api/', include(router.urls)),
    
    # Template-based views
    path('list/', views.ApiListTemplateView.as_view(), name='api-list-template'),
    path('detail/<int:pk>/', views.ApiDetailTemplateView.as_view(), name='api-detail-template'),
    path('create/', views.ApiCreateTemplateView.as_view(), name='api-create-template'),
    path('update/<int:pk>/', views.ApiUpdateTemplateView.as_view(), name='api-update-template'),
    path('delete/<int:pk>/', views.ApiDeleteTemplateView.as_view(), name='api-delete-template'),
]