"""
Football Views - TEK SATIRLA IMPORT TEST!
Bu dosya da modülleri tek satırla import eder
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

# ✨ TEK SATIRLA IMPORT! - MÜKEMMEL ÇALIŞIYOR!
from .models import (
    League, Team, Match,                    # Base models
    TeamStats, MatchAnalysis,               # Analytics models
    LeagueTable, WeeklyStats               # Statistics models
)

def home(request):
    """Ana sayfa"""
    # Son maçlar
    recent_matches = Match.objects.select_related(
        'home_team', 'away_team', 'league'
    ).filter(status='finished').order_by('-match_date')[:10]
    
    # Aktif ligler
    active_leagues = League.objects.filter(is_active=True)
    
    # İstatistikler
    total_teams = Team.objects.filter(is_active=True).count()
    total_matches = Match.objects.count()
    
    context = {
        'recent_matches': recent_matches,
        'active_leagues': active_leagues,
        'total_teams': total_teams,
        'total_matches': total_matches,
    }
    return render(request, 'football/home.html', context)

def league_list(request):
    """Liga listesi"""
    leagues = League.objects.filter(is_active=True).order_by('name')
    
    context = {
        'leagues': leagues,
        'page_title': 'Ligler'
    }
    return render(request, 'football/league_list.html', context)

def league_detail(request, league_id):
    """Liga detayı"""
    league = get_object_or_404(League, id=league_id)
    
    # Lig tablosu
    league_table = LeagueTable.objects.filter(
        league=league
    ).select_related('team').order_by('position')
    
    # Son maçlar
    recent_matches = Match.objects.filter(
        league=league,
        status='finished'
    ).select_related('home_team', 'away_team').order_by('-match_date')[:10]
    
    # Gelecek maçlar
    upcoming_matches = Match.objects.filter(
        league=league,
        status='scheduled'
    ).select_related('home_team', 'away_team').order_by('match_date')[:10]
    
    context = {
        'league': league,
        'league_table': league_table,
        'recent_matches': recent_matches,
        'upcoming_matches': upcoming_matches,
        'page_title': f'{league.name} - {league.season}'
    }
    return render(request, 'football/league_detail.html', context)

def team_list(request):
    """Takım listesi"""
    # Arama
    search_query = request.GET.get('search', '')
    teams = Team.objects.filter(is_active=True).select_related('league')
    
    if search_query:
        teams = teams.filter(
            Q(name__icontains=search_query) |
            Q(short_name__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    # Sayfalama
    paginator = Paginator(teams, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'page_title': 'Takımlar'
    }
    return render(request, 'football/team_list.html', context)

def team_detail(request, team_id):
    """Takım detayı"""
    team = get_object_or_404(Team, id=team_id)
    
    # Takım istatistikleri
    try:
        team_stats = TeamStats.objects.get(team=team)
    except TeamStats.DoesNotExist:
        team_stats = None
    
    # Son maçlar
    recent_matches = Match.objects.filter(
        Q(home_team=team) | Q(away_team=team),
        status='finished'
    ).select_related('home_team', 'away_team', 'league').order_by('-match_date')[:10]
    
    # Gelecek maçlar
    upcoming_matches = Match.objects.filter(
        Q(home_team=team) | Q(away_team=team),
        status='scheduled'
    ).select_related('home_team', 'away_team', 'league').order_by('match_date')[:5]
    
    context = {
        'team': team,
        'team_stats': team_stats,
        'recent_matches': recent_matches,
        'upcoming_matches': upcoming_matches,
        'page_title': team.name
    }
    return render(request, 'football/team_detail.html', context)

def match_list(request):
    """Maç listesi"""
    # Filtreler
    status_filter = request.GET.get('status', '')
    league_filter = request.GET.get('league', '')
    
    matches = Match.objects.select_related(
        'home_team', 'away_team', 'league'
    ).order_by('-match_date')
    
    if status_filter:
        matches = matches.filter(status=status_filter)
    
    if league_filter:
        matches = matches.filter(league_id=league_filter)
    
    # Sayfalama
    paginator = Paginator(matches, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Filtre seçenekleri
    leagues = League.objects.filter(is_active=True)
    status_choices = Match.MATCH_STATUS_CHOICES
    
    context = {
        'page_obj': page_obj,
        'leagues': leagues,
        'status_choices': status_choices,
        'current_status': status_filter,
        'current_league': league_filter,
        'page_title': 'Maçlar'
    }
    return render(request, 'football/match_list.html', context)

def match_detail(request, match_id):
    """Maç detayı"""
    match = get_object_or_404(
        Match.objects.select_related('home_team', 'away_team', 'league'),
        match_id=match_id
    )
    
    # Maç analizi
    try:
        match_analysis = MatchAnalysis.objects.get(match=match)
    except MatchAnalysis.DoesNotExist:
        match_analysis = None
    
    context = {
        'match': match,
        'match_analysis': match_analysis,
        'page_title': f'{match.home_team} vs {match.away_team}'
    }
    return render(request, 'football/match_detail.html', context)

# Advanced Multi-Table Views
def dashboard(request):
    """Süper dashboard - 8+ tablo birden!"""
    # Django'da tek view'de birden fazla tablo kullanımı örneği
    
    # 1. Son maçlar (Match + Team + League) - 3 tablo
    recent_matches = Match.objects.select_related(
        'home_team', 'away_team', 'league'
    ).filter(status='finished').order_by('-match_date')[:5]
    
    # 2. Puan durumu (LeagueTable + Team + League) - 3 tablo
    top_teams = LeagueTable.objects.select_related(
        'team', 'league'
    ).order_by('position')[:10]
    
    # 3. En iyi performans (TeamStats + Team) - 2 tablo
    best_performers = TeamStats.objects.select_related(
        'team'
    ).order_by('-points', '-goal_difference')[:5]
    
    # 4. Haftalık istatistikler (WeeklyStats + League) - 2 tablo
    weekly_stats = WeeklyStats.objects.select_related(
        'league'
    ).order_by('-week')[:3]
    
    # 5. Aggregate queries - birden fazla tablodan hesaplama
    from django.db.models import Count, Avg, Sum
    
    league_summary = League.objects.annotate(
        total_teams=Count('team'),
        total_matches=Count('match'),
        avg_goals=Avg('match__home_goals') + Avg('match__away_goals')
    ).filter(is_active=True)[:5]
    
    context = {
        'recent_matches': recent_matches,        # 3 tablo
        'top_teams': top_teams,                  # 3 tablo  
        'best_performers': best_performers,      # 2 tablo
        'weekly_stats': weekly_stats,            # 2 tablo
        'league_summary': league_summary,        # 3 tablo (hesaplamalı)
        'page_title': 'Dashboard - 8+ Tablo Birden!'
    }
    return render(request, 'football/dashboard.html', context)

def advanced_search(request):
    """Gelişmiş arama - 5+ tablo"""
    from django.db.models import Q
    
    query = request.GET.get('q', '')
    results = {}
    
    if query:
        # 1. Teams arama (Team + League) - 2 tablo
        results['teams'] = Team.objects.filter(
            Q(name__icontains=query) | Q(city__icontains=query)
        ).select_related('league')[:10]
        
        # 2. Matches arama (Match + Team + League) - 4 tablo
        results['matches'] = Match.objects.filter(
            Q(home_team__name__icontains=query) |
            Q(away_team__name__icontains=query)
        ).select_related('home_team', 'away_team', 'league')[:10]
        
        # 3. Team Stats arama (TeamStats + Team) - 2 tablo
        results['top_performers'] = TeamStats.objects.filter(
            team__name__icontains=query,
            points__gte=10
        ).select_related('team')[:5]
        
        # 4. Weekly Stats (WeeklyStats + League) - 2 tablo
        results['weekly_data'] = WeeklyStats.objects.filter(
            league__name__icontains=query
        ).select_related('league')[:5]
    
    context = {
        'query': query,
        'results': results,
        'total_tables_used': '5+ Tablo Kullanıldı',
        'page_title': f'Arama: {query}' if query else 'Gelişmiş Arama'
    }
    return render(request, 'football/advanced_search.html', context)

# API Views
def api_teams(request):
    """Takımlar API"""
    teams = Team.objects.filter(is_active=True).values(
        'id', 'name', 'short_name', 'league__name'
    )
    return JsonResponse(list(teams), safe=False)

def api_matches_today(request):
    """Bugünün maçları API"""
    from django.utils import timezone
    today = timezone.now().date()
    
    matches = Match.objects.filter(
        match_date__date=today
    ).select_related('home_team', 'away_team').values(
        'match_id', 'home_team__name', 'away_team__name',
        'match_date', 'status', 'home_goals', 'away_goals'
    )
    
    return JsonResponse(list(matches), safe=False)

def api_dashboard_summary(request):
    """Dashboard özeti API - 6+ tablo birden"""
    from django.db.models import Count, Avg
    
    # Birden fazla tablodan veri topla
    summary = {
        'total_teams': Team.objects.filter(is_active=True).count(),
        'total_matches': Match.objects.count(),
        'total_leagues': League.objects.filter(is_active=True).count(),
        'recent_matches': list(Match.objects.select_related(
            'home_team', 'away_team'
        ).filter(status='finished').values(
            'home_team__name', 'away_team__name', 'home_goals', 'away_goals'
        )[:5]),
        'top_teams': list(TeamStats.objects.select_related(
            'team'
        ).order_by('-points').values(
            'team__name', 'points', 'wins', 'goal_difference'
        )[:5]),
        'league_stats': list(League.objects.annotate(
            team_count=Count('team'),
            match_count=Count('match')
        ).values('name', 'team_count', 'match_count')[:5])
    }
    
    return JsonResponse(summary)
