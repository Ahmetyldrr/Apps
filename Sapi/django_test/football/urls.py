"""
Football URLs
"""
from django.urls import path
from . import views

app_name = 'football'

urlpatterns = [
    # Ana sayfalar
    path('', views.home, name='home'),
    
    # Multi-table views (Birden fazla tablo örneği)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.advanced_search, name='advanced_search'),
    
    # Liga URLs
    path('leagues/', views.league_list, name='league_list'),
    path('leagues/<int:league_id>/', views.league_detail, name='league_detail'),
    
    # Takım URLs
    path('teams/', views.team_list, name='team_list'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    
    # Maç URLs
    path('matches/', views.match_list, name='match_list'),
    path('matches/<int:match_id>/', views.match_detail, name='match_detail'),
    
    # API URLs
    path('api/teams/', views.api_teams, name='api_teams'),
    path('api/matches/today/', views.api_matches_today, name='api_matches_today'),
    path('api/dashboard/', views.api_dashboard_summary, name='api_dashboard'),
]
