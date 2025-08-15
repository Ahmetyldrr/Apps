"""
Football Models Package
Bu paket tüm football modellerini tek satırla import etmenizi sağlar

Kullanım:
    from football.models import Team, Match, TeamStats
    from football.models import League, MatchAnalysis
    from football.models import *  # Hepsini import et
"""

# ========== BASE MODELS ==========
from .base import (
    League,
    Team, 
    Match,
    Player
)

# ========== ANALYTICS MODELS ==========
from .analytics import (
    TeamStats,
    MatchAnalysis,
    PlayerStats,
    LeagueAnalysis
)

# ========== STATISTICS MODELS ==========
from .statistics import (
    LeagueTable,
    WeeklyStats,
    MonthlyStats,
    GoalStats,
    SeasonStats
)

# Django için tüm modelleri export et
__all__ = [
    # Base models - Temel modeller
    'League',
    'Team', 
    'Match',
    'Player',
    
    # Analytics models - Analiz modelleri
    'TeamStats',
    'MatchAnalysis', 
    'PlayerStats',
    'LeagueAnalysis',
    
    # Statistics models - İstatistik modelleri
    'LeagueTable',
    'WeeklyStats',
    'MonthlyStats', 
    'GoalStats',
    'SeasonStats'
]

# Model kategorileri için gruplar
BASE_MODELS = ['League', 'Team', 'Match', 'Player']
ANALYTICS_MODELS = ['TeamStats', 'MatchAnalysis', 'PlayerStats', 'LeagueAnalysis'] 
STATISTICS_MODELS = ['LeagueTable', 'WeeklyStats', 'MonthlyStats', 'GoalStats', 'SeasonStats']
