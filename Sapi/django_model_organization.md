# 🏗️ Django Model Organizasyonu - Temel vs Analiz Modelleri

## 📊 DJANGO MODEL ORGANİZASYON SEÇENEKLERİ

### 🎯 SEÇENEK 1: Tek models.py (Basit Yaklaşım)
```python
# football/models.py
from django.db import models

# ========== TEMEL MODELLER ==========
class League(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    
class Team(models.Model):
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    
class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_matches')
    away_team = models.ForeignKey(Team, related_name='away_matches')
    match_date = models.DateTimeField()
    home_goals = models.IntegerField(default=0)
    away_goals = models.IntegerField(default=0)

# ========== ANALİZ MODELLERİ ==========
class TeamStats(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    total_matches = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)
    
class MatchAnalysis(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    possession_home = models.FloatField(null=True)
    possession_away = models.FloatField(null=True)
    shots_home = models.IntegerField(default=0)
    shots_away = models.IntegerField(default=0)
    
class LeagueAnalysis(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    season = models.CharField(max_length=10)
    average_goals = models.FloatField()
    total_matches = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### 🔧 SEÇENEK 2: Ayrı Dosyalar (Modüler Yaklaşım) - TAVSİYE EDİLEN!
```
football/
├── models/
│   ├── __init__.py          # Tüm modelleri import eder
│   ├── base.py              # Temel modeller
│   ├── analytics.py         # Analiz modelleri
│   ├── statistics.py        # İstatistik modelleri
│   └── reports.py           # Rapor modelleri
├── admin.py
├── views.py
└── management/
    └── commands/
```

#### models/__init__.py
```python
# football/models/__init__.py
from .base import League, Team, Match, Player
from .analytics import TeamStats, MatchAnalysis, PlayerStats
from .statistics import LeagueTable, GoalStats, WeeklyStats
from .reports import MonthlyReport, SeasonReport

# Django için tüm modelleri export et
__all__ = [
    # Base models
    'League', 'Team', 'Match', 'Player',
    # Analytics models  
    'TeamStats', 'MatchAnalysis', 'PlayerStats',
    # Statistics models
    'LeagueTable', 'GoalStats', 'WeeklyStats',
    # Report models
    'MonthlyReport', 'SeasonReport'
]
```

#### models/base.py (Temel Modeller)
```python
# football/models/base.py
from django.db import models

class League(models.Model):
    """Temel lig modeli"""
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    season = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'leagues'
        verbose_name = 'Liga'
        verbose_name_plural = 'Ligalar'
    
    def __str__(self):
        return f"{self.name} ({self.season})"

class Team(models.Model):
    """Temel takım modeli"""
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    founded_year = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'teams'
        unique_together = ['name', 'league']
    
    def __str__(self):
        return self.name

class Match(models.Model):
    """Temel maç modeli"""
    MATCH_STATUS = [
        ('scheduled', 'Planlandı'),
        ('live', 'Canlı'),
        ('finished', 'Bitti'),
        ('postponed', 'Ertelendi'),
    ]
    
    match_id = models.IntegerField(unique=True)
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    match_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=MATCH_STATUS, default='scheduled')
    home_goals = models.IntegerField(default=0)
    away_goals = models.IntegerField(default=0)
    week = models.IntegerField(null=True)
    
    class Meta:
        db_table = 'matches'
        ordering = ['-match_date']
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
```

#### models/analytics.py (Analiz Modelleri)  
```python
# football/models/analytics.py
from django.db import models
from .base import Team, Match, League

class TeamStats(models.Model):
    """Takım istatistikleri"""
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    season = models.CharField(max_length=10)
    
    # Temel istatistikler
    matches_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    
    # Gol istatistikleri
    goals_scored = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)
    
    # Hesaplanan alanlar
    points = models.IntegerField(default=0)
    goal_difference = models.IntegerField(default=0)
    
    # Analiz tarihi
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'team_stats'
        unique_together = ['team', 'season']
    
    def calculate_stats(self):
        """İstatistikleri hesapla"""
        self.points = (self.wins * 3) + self.draws
        self.goal_difference = self.goals_scored - self.goals_conceded
        self.save()

class MatchAnalysis(models.Model):
    """Maç analizi"""
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    
    # Possession analizi
    possession_home = models.FloatField(null=True, blank=True)
    possession_away = models.FloatField(null=True, blank=True)
    
    # Şut analizi
    shots_home = models.IntegerField(default=0)
    shots_away = models.IntegerField(default=0)
    shots_on_target_home = models.IntegerField(default=0)
    shots_on_target_away = models.IntegerField(default=0)
    
    # Kart analizi
    yellow_cards_home = models.IntegerField(default=0)
    yellow_cards_away = models.IntegerField(default=0)
    red_cards_home = models.IntegerField(default=0)
    red_cards_away = models.IntegerField(default=0)
    
    # Analiz skorları
    performance_score_home = models.FloatField(null=True)
    performance_score_away = models.FloatField(null=True)
    
    class Meta:
        db_table = 'match_analysis'

class LeagueAnalysis(models.Model):
    """Lig analizi"""
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    analysis_date = models.DateField()
    
    # Lig istatistikleri
    total_matches = models.IntegerField()
    total_goals = models.IntegerField()
    average_goals_per_match = models.FloatField()
    
    # En yüksek skorlar
    highest_scoring_match = models.ForeignKey(Match, null=True, on_delete=models.SET_NULL)
    most_wins_team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'league_analysis'
        unique_together = ['league', 'analysis_date']
```

#### models/statistics.py (İstatistik Modelleri)
```python
# football/models/statistics.py
from django.db import models
from .base import League, Team

class LeagueTable(models.Model):
    """Lig tablosu"""
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.IntegerField()
    points = models.IntegerField()
    matches_played = models.IntegerField()
    goal_difference = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'league_table'
        unique_together = ['league', 'team']
        ordering = ['position']

class WeeklyStats(models.Model):
    """Haftalık istatistikler"""
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    week = models.IntegerField()
    total_goals = models.IntegerField(default=0)
    total_matches = models.IntegerField(default=0)
    biggest_win_margin = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'weekly_stats'
        unique_together = ['league', 'week']
```

## 🎯 BENİM TAVSİYEM: AYRI DOSYALAR!

### ✅ Avantajları:
1. **Temiz kod**: Her dosya tek sorumluluk
2. **Kolay bulma**: Hangi model nerede belli
3. **Team work**: Farklı kişiler farklı dosyalarda çalışabilir
4. **Maintainability**: Değişiklik yapmak kolay
5. **Import flexibility**: Sadece ihtiyacınız olanı import edin

### 🚀 Kullanım Örnekleri:
```python
# Sadece temel modelleri import et
from football.models.base import Team, Match

# Sadece analiz modellerini import et  
from football.models.analytics import TeamStats, MatchAnalysis

# Hepsini import et
from football.models import Team, TeamStats, MatchAnalysis
```

## 📋 ÖNERİLEN YAPILANDIRMA:

```
football/models/
├── __init__.py              # Tüm export'lar
├── base.py                  # League, Team, Match, Player
├── analytics.py             # TeamStats, MatchAnalysis, PlayerStats  
├── statistics.py            # LeagueTable, WeeklyStats, MonthlyStats
├── reports.py               # Rapor modelleri
└── utils.py                 # Ortak model utilities
```

## 🎉 SONUÇ

**Ayrı dosyalar yaklaşımı** daha profesyonel ve maintainable!

**Bu yapıyla Django projesi kuralım mı?** 🚀
