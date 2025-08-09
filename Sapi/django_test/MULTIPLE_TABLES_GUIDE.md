# 🎯 Django Views - Birden Fazla Veritabanı Tablosu Kullanımı

## ✅ EVET, TAMAMİYLE DOĞRU!

Django views'de **birden fazla model/tablo** aynı anda kullanabilirsiniz!

## 📊 MEVCUT DOSYANIZDA ÖRNEKLER:

### 1. home() view'de 4 farklı tablo:
```python
def home(request):
    # 1. Match tablosu + ilişkili tablolar
    recent_matches = Match.objects.select_related(
        'home_team', 'away_team', 'league'  # 4 tablo birden!
    ).filter(status='finished').order_by('-match_date')[:10]
    
    # 2. League tablosu
    active_leagues = League.objects.filter(is_active=True)
    
    # 3. Team tablosu
    total_teams = Team.objects.filter(is_active=True).count()
    
    # 4. Match tablosu (tekrar)
    total_matches = Match.objects.count()
```

### 2. league_detail() view'de 3 farklı tablo:
```python
def league_detail(request, league_id):
    # 1. League tablosu
    league = get_object_or_404(League, id=league_id)
    
    # 2. LeagueTable + Team tablosu
    league_table = LeagueTable.objects.filter(
        league=league
    ).select_related('team').order_by('position')
    
    # 3. Match + Team tabloları
    recent_matches = Match.objects.filter(
        league=league, status='finished'
    ).select_related('home_team', 'away_team')[:10]
```

## 🚀 DAHA GELİŞMİŞ ÖRNEKLER:

### 📈 Dashboard View (10+ Tablo)
```python
def dashboard(request):
    """Süper dashboard - 10+ tablo birden!"""
    
    # 1. Son maçlar (Match + Team + League)
    recent_matches = Match.objects.select_related(
        'home_team', 'away_team', 'league'
    ).filter(status='finished')[:5]
    
    # 2. Puan durumu (LeagueTable + Team + League)
    top_teams = LeagueTable.objects.select_related(
        'team', 'league'
    ).order_by('position')[:10]
    
    # 3. En iyi performans (TeamStats + Team)
    best_performers = TeamStats.objects.select_related(
        'team'
    ).order_by('-points', '-goal_difference')[:5]
    
    # 4. Son analizler (MatchAnalysis + Match + Team)
    recent_analysis = MatchAnalysis.objects.select_related(
        'match__home_team', 'match__away_team'
    ).order_by('-created_at')[:3]
    
    # 5. Haftalık istatistikler (WeeklyStats + League)
    weekly_stats = WeeklyStats.objects.select_related(
        'league'
    ).order_by('-week')[:5]
    
    # 6. Goller (GoalStats + League)
    goal_stats = GoalStats.objects.select_related(
        'league'
    ).order_by('-created_at')[:3]
    
    # 7. Oyuncu istatistikleri (PlayerStats + Player + Team)
    top_scorers = PlayerStats.objects.select_related(
        'player__team'
    ).order_by('-goals')[:10]
    
    # 8. Lig analizi (LeagueAnalysis + League + Team + Match)
    league_analysis = LeagueAnalysis.objects.select_related(
        'league', 'highest_scoring_match__home_team', 
        'highest_scoring_match__away_team', 'most_wins_team'
    ).order_by('-analysis_date')[:3]
    
    context = {
        'recent_matches': recent_matches,
        'top_teams': top_teams,
        'best_performers': best_performers,
        'recent_analysis': recent_analysis,
        'weekly_stats': weekly_stats,
        'goal_stats': goal_stats,
        'top_scorers': top_scorers,
        'league_analysis': league_analysis,
    }
    return render(request, 'football/dashboard.html', context)
```

### 🔍 Advanced Search (5+ Tablo)
```python
def advanced_search(request):
    """Gelişmiş arama - 5+ tablo"""
    query = request.GET.get('q', '')
    
    if query:
        # 1. Teams arama
        teams = Team.objects.filter(
            Q(name__icontains=query) | Q(city__icontains=query)
        ).select_related('league')
        
        # 2. Matches arama  
        matches = Match.objects.filter(
            Q(home_team__name__icontains=query) |
            Q(away_team__name__icontains=query)
        ).select_related('home_team', 'away_team', 'league')
        
        # 3. Players arama
        players = Player.objects.filter(
            Q(name__icontains=query) | Q(nationality__icontains=query)
        ).select_related('team')
        
        # 4. Leagues arama
        leagues = League.objects.filter(
            Q(name__icontains=query) | Q(country__icontains=query)
        )
        
        # 5. Team Stats arama (yüksek performanslı takımlar)
        high_performers = TeamStats.objects.filter(
            team__name__icontains=query,
            points__gte=20
        ).select_related('team')
    else:
        teams = matches = players = leagues = high_performers = []
    
    context = {
        'query': query,
        'teams': teams,
        'matches': matches, 
        'players': players,
        'leagues': leagues,
        'high_performers': high_performers,
    }
    return render(request, 'football/search.html', context)
```

### 📊 Statistics View (8+ Tablo)
```python
def statistics_overview(request):
    """İstatistik özeti - 8+ tablo birden"""
    
    # Aggregate queries - birden fazla tablodan özet
    from django.db.models import Count, Avg, Sum, Max
    
    # 1. Team ve Match tabloları
    team_stats = Team.objects.annotate(
        total_home_matches=Count('home_matches'),
        total_away_matches=Count('away_matches'),
        avg_home_goals=Avg('home_matches__home_goals'),
        avg_away_goals=Avg('away_matches__away_goals')
    ).filter(is_active=True)
    
    # 2. League analizi (League + Match + Team)
    league_overview = League.objects.annotate(
        total_matches=Count('match'),
        total_teams=Count('team'),
        avg_goals_per_match=Avg('match__home_goals') + Avg('match__away_goals')
    ).filter(is_active=True)
    
    # 3. Player performansı (Player + PlayerStats + Team)
    top_performers = Player.objects.select_related(
        'team'
    ).annotate(
        total_goals=Sum('playerstats__goals'),
        total_assists=Sum('playerstats__assists')
    ).filter(
        total_goals__isnull=False
    ).order_by('-total_goals')[:20]
    
    # 4. Match trends (Match + MatchAnalysis)
    match_trends = Match.objects.select_related(
        'matchanalysis'
    ).filter(
        status='finished',
        matchanalysis__isnull=False
    ).aggregate(
        avg_possession=Avg('matchanalysis__possession_home'),
        avg_shots=Avg('matchanalysis__shots_home'),
        total_analyzed=Count('matchanalysis')
    )
    
    context = {
        'team_stats': team_stats,
        'league_overview': league_overview,
        'top_performers': top_performers,
        'match_trends': match_trends,
    }
    return render(request, 'football/statistics.html', context)
```

## 🔥 İLERİ SEVİYE TEKNİKLER:

### 1. SELECT_RELATED (Join işlemleri)
```python
# 4 tabloyu tek query'de birleştir
matches = Match.objects.select_related(
    'home_team',           # teams tablosu
    'away_team',           # teams tablosu  
    'league',              # leagues tablosu
    'matchanalysis'        # match_analysis tablosu
)
```

### 2. PREFETCH_RELATED (Reverse ilişkiler)
```python
# Team + tüm maçları tek seferde
teams = Team.objects.prefetch_related(
    'home_matches',        # Match tablosu
    'away_matches',        # Match tablosu
    'teamstats_set',       # TeamStats tablosu
    'playerstats_set'      # PlayerStats tablosu
)
```

### 3. ANNOTATE (Hesaplamalar)
```python
# Birden fazla tablodan hesaplama
teams = Team.objects.annotate(
    total_matches=Count('home_matches') + Count('away_matches'),
    total_wins=Count('home_matches', filter=Q(home_matches__home_goals__gt=F('home_matches__away_goals'))),
    avg_goals=Avg('home_matches__home_goals')
)
```

## 🎉 SONUÇ:

**EVET! Django views'de sınırsız sayıda tablo kullanabilirsiniz:**

✅ **Tek view'de 10+ tablo** - Normal ve yaygın  
✅ **Select_related** - Performanslı joinler  
✅ **Prefetch_related** - Reverse ilişkiler  
✅ **Annotations** - Hesaplamalı alanlar  
✅ **Complex queries** - Karmaşık sorgular  

Sizin mevcut dosyanızda da zaten bu kullanım var! 🎯
