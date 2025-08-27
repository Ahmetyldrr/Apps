from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Template views
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterTemplateView.as_view(), name='register'),
    path('profile/', views.ProfileTemplateView.as_view(), name='profile'),
    
    # API endpoints
    path('api/register/', views.RegisterView.as_view(), name='api-register'),
    path('api/login/', views.LoginView.as_view(), name='api-login'),
    path('api/logout/', views.LogoutView.as_view(), name='api-logout'),
    path('api/profile/', views.ProfileView.as_view(), name='api-profile'),
]